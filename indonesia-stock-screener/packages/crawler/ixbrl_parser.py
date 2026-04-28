import defusedxml.ElementTree as ET
from defusedxml.common import DefusedXmlException
import os
import random

class iXBRLParser:
    def __init__(self):
        self.namespace = {
            "ix": "http://www.xbrl.org/2013/inlineXBRL",
            "idx": "http://www.idx.co.id/xbrl/taxonomy/2019-01-01"
        }

    async def download_and_extract(self, url: str) -> str:
        """
        Mock function to represent downloading the ZIP and extracting the XML.
        """
        print(f"[Parser] Simulating download from {url}")
        return "mocked_path.xml"

    def parse_document(self, ticker: str, filepath: str, year: int = 2023, quarter: str = "Q4"):
        """
        Parses iXBRL XML. If filepath doesn't exist (mocking), returns dummy structured data.
        """
        if not os.path.exists(filepath):
            print(f"[Parser] Real XML not found. Generating mock fundamental data for {ticker}")
            # Mock Data aligned with PRD requirements
            revenue = random.uniform(50000, 150000) * 1_000_000_000
            net_income = revenue * random.uniform(0.1, 0.4)
            return {
                "ticker": ticker,
                "year": year,
                "quarter": quarter,
                "fundamentals": {
                    "total_revenue": int(revenue), 
                    "net_income": int(net_income),
                    "operating_cash_flow": int(net_income * 1.1),
                    "total_assets": int(revenue * 4.5),
                    "total_equity": int(revenue * 1.5),
                    "shares_outstanding": int(random.uniform(10_000, 150_000) * 1_000_000)
                }
            }

        # Real Extraction Logic
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        try:
            root = ET.fromstring(content)
        except DefusedXmlException as e:
            print(f"[Parser] Security error parsing XML for {ticker}: {e}")
            root = None
        except ET.ParseError as e:
            print(f"[Parser] Parse error for {ticker}: {e}")
            root = None

        fundamentals = {}
        if root is not None:
            # Exact taxonomy tags vary by IDX release
            mapping = {
                "idx:TotalRevenue": "total_revenue",
                "idx:ProfitLoss": "net_income",
                "idx:NetCashFlowsFromOperatingActivities": "operating_cash_flow",
                "idx:TotalAssets": "total_assets",
                "idx:TotalEquity": "total_equity"
            }

            for tag, key in mapping.items():
                elements = root.findall(f".//*[@name='{tag}']")
                if elements and elements[0].text:
                    value_str = elements[0].text.strip().replace(',', '')
                    try:
                        fundamentals[key] = float(value_str)
                    except ValueError:
                        fundamentals[key] = 0.0
                else:
                    fundamentals[key] = 0.0

            shares = root.findall(".//*[@name='idx:NumberOfSharesOutstanding']")
            if shares and shares[0].text:
                 fundamentals["shares_outstanding"] = float(shares[0].text.strip().replace(',', ''))
            else:
                 fundamentals["shares_outstanding"] = 0.0
        else:
            # Fallback if parsing fails
            fundamentals = {
                "total_revenue": 0.0,
                "net_income": 0.0,
                "operating_cash_flow": 0.0,
                "total_assets": 0.0,
                "total_equity": 0.0,
                "shares_outstanding": 0.0
            }

        return {
            "ticker": ticker,
            "year": year,
            "quarter": quarter,
            "fundamentals": fundamentals
        }

