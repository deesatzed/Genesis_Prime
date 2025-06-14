#!/usr/bin/env python
"""
Database setup script for Thousand Questions system
Sets up PostgreSQL database with schema and loads questions
"""

import os
import asyncio
import psycopg
from pathlib import Path

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:pass@localhost:5432/sentient")

async def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to postgres database to create sentient database
        base_url = DATABASE_URL.rsplit('/', 1)[0] + '/postgres'
        conn = await psycopg.AsyncConnection.connect(base_url)
        await conn.set_autocommit(True)
        
        # Check if database exists
        result = await conn.execute("""
            SELECT 1 FROM pg_database WHERE datname = 'sentient'
        """)
        
        if not result:
            await conn.execute("CREATE DATABASE sentient")
            print("✅ Created database 'sentient'")
        else:
            print("ℹ️ Database 'sentient' already exists")
            
        await conn.close()
        
    except Exception as e:
        print(f"⚠️ Could not create database (may already exist): {e}")

async def run_schema():
    """Execute all *.sql schema files in the database directory"""
    db_dir = Path(__file__).parent / "database"
    sql_files = sorted(db_dir.glob("*.sql"))
    if not sql_files:
        print(f"❌ No .sql schema files found in {db_dir}")
        return False

    try:
        conn = await psycopg.AsyncConnection.connect(DATABASE_URL)
        for sql_file in sql_files:
            print(f"⚙️  Applying schema: {sql_file.name}")
            with open(sql_file, "r") as f:
                sql = f.read()
            await conn.execute(sql)
        await conn.close()
        print("✅ All schema files applied")
        return True
    except Exception as e:
        print(f"❌ Error applying schema files: {e}")
        return False

async def load_questions():
    """Load questions from the generated SQL file"""
    sql_path = Path(__file__).parent.parent.parent / "libs" / "tq_dataset" / "tq_questions.sql"
    
    if not sql_path.exists():
        print(f"❌ Questions SQL file not found: {sql_path}")
        print("Run: python -m libs.tq_dataset.parse_tq --infile libs/tq_dataset/Thousand_Questions.txt --sql-out libs/tq_dataset/tq_questions.sql")
        return False
    
    with open(sql_path, 'r') as f:
        questions_sql = f.read()
    
    try:
        conn = await psycopg.AsyncConnection.connect(DATABASE_URL)
        await conn.execute(questions_sql)
        await conn.close()
        print("✅ Questions loaded into database")
        return True
    except Exception as e:
        print(f"❌ Error loading questions: {e}")
        return False

async def verify_setup():
    """Verify the database setup"""
    try:
        conn = await psycopg.AsyncConnection.connect(DATABASE_URL)
        
        # Count questions
        result = await conn.fetchrow("SELECT COUNT(*) as count FROM tq_questions")
        question_count = result["count"] if result else 0
        
        # Check tables exist
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        
        await conn.close()
        
        print(f"\n📊 Database Verification:")
        print(f"   Questions loaded: {question_count}")
        print(f"   Tables created: {len(tables)}")
        print(f"   Tables: {', '.join([t['table_name'] for t in tables])}")
        
        return question_count > 0
        
    except Exception as e:
        print(f"❌ Error verifying setup: {e}")
        return False

async def main():
    """Main setup function"""
    print("🚀 Setting up Thousand Questions database...")
    print(f"Database URL: {DATABASE_URL}")
    
    # Step 1: Create database
    await create_database()
    
    # Step 2: Run schema
    if not await run_schema():
        return
    
    # Step 3: Load questions
    if not await load_questions():
        return
    
    # Step 4: Verify setup
    if await verify_setup():
        print("\n🎉 Database setup completed successfully!")
        print("\nYou can now run:")
        print("   python cli.py --demo")
        print("   python cli.py --interactive")
    else:
        print("\n❌ Database setup verification failed")

if __name__ == "__main__":
    asyncio.run(main())