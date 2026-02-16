import asyncio
import asyncpg
import urllib.parse

# DB credentials
password = "YOUR PASSWORD"
encoded_password = urllib.parse.quote(password)
DATABASE_URL = f"postgresql://postgres:{encoded_password}@XYZ"

async def main():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        # Drop old tables
        await conn.execute("DROP TABLE IF EXISTS financial_reports;")
        await conn.execute("DROP TABLE IF EXISTS companies;")
        
        # Create tables
        await conn.execute("""
            CREATE TABLE companies (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                ticker TEXT NOT NULL,
                industry TEXT,
                valuation TEXT
            );
        """)
        await conn.execute("""
            CREATE TABLE financial_reports (
                id SERIAL PRIMARY KEY,
                company_id INT REFERENCES companies(id) ON DELETE CASCADE,
                fiscal_year TEXT,
                revenue TEXT,
                profit TEXT
            );
        """)

        # Insert 5 companies
        await conn.execute("""
            INSERT INTO companies (id, name, ticker, industry, valuation) VALUES
            (1,'Apple Inc','AAPL','Technology','3T'),
            (2,'Microsoft Corp','MSFT','Technology','2.5T'),
            (3,'Amazon.com Inc','AMZN','E-commerce','1.7T'),
            (4,'Alphabet Inc','GOOGL','Technology','1.6T'),
            (5,'Tesla Inc','TSLA','Automotive','900B')
            ON CONFLICT DO NOTHING;
        """)

        # Insert financial reports
        await conn.execute("""
            INSERT INTO financial_reports (company_id,fiscal_year,revenue,profit) VALUES
            (1,'2025','400B','100B'),
            (2,'2025','350B','90B'),
            (3,'2025','500B','80B'),
            (4,'2025','300B','70B'),
            (5,'2025','120B','20B');
        """)

        print("✅ DB ready with 5 companies and financial reports!")
    finally:
        await conn.close()

asyncio.run(main())
