#!/usr/bin/env python3
"""
India FinTech Platform - Interactive Demo

This demo showcases all three missing financial products:
1. Earned Wage Access (EWA)
2. Income Share Agreements (ISA)
3. Parametric Insurance

Run with: python demo/run_demo.py
"""

import sys
sys.path.insert(0, '/workspace/india_fintech_platform')

from datetime import datetime, date, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich import print as rprint
import time

from core.models import User, KYCStatus, EmploymentType
from core.database import db
from services.credit_identity import credit_identity_service
from services.income_verification import income_verification_service
from services.collection import collection_service
from products.earned_wage_access import ewa_product
from products.income_share_agreement import isa_product
from products.parametric_insurance import parametric_insurance_product, InsuranceType

console = Console()


def print_header(title: str):
    console.print()
    console.print(Panel(f"[bold blue]{title}[/bold blue]", expand=False))
    console.print()


def print_success(message: str):
    console.print(f"[green]✓[/green] {message}")


def print_info(message: str):
    console.print(f"[blue]ℹ[/blue] {message}")


def print_warning(message: str):
    console.print(f"[yellow]⚠[/yellow] {message}")


def simulate_delay(seconds: float = 0.5):
    time.sleep(seconds)


def create_demo_users():
    """Create demo users representing different segments"""
    print_header("👥 Creating Demo Users")
    
    users = []
    
    # User 1: Ramesh - Daily wage worker (from the AI debate)
    ramesh = User(
        name="Ramesh Kumar",
        phone="9876543210",
        date_of_birth=date(1985, 3, 15),
        state="Maharashtra",
        district="Mumbai",
        employment_type=EmploymentType.DAILY_WAGE,
        monthly_income=12000,
        kyc_status=KYCStatus.VERIFIED,
        kyc_verified_at=datetime.now(),
    )
    db.create_user(ramesh)
    credit_identity_service.create_profile(ramesh)
    users.append(ramesh)
    print_success(f"Created: {ramesh.name} (Daily Wage Worker, ₹12,000/month)")
    
    # User 2: Priya - Gig worker (Swiggy/Zomato)
    priya = User(
        name="Priya Sharma",
        phone="9876543211",
        date_of_birth=date(1995, 7, 22),
        state="Karnataka",
        district="Bangalore",
        employment_type=EmploymentType.GIG_WORKER,
        monthly_income=25000,
        kyc_status=KYCStatus.VERIFIED,
        kyc_verified_at=datetime.now(),
    )
    db.create_user(priya)
    credit_identity_service.create_profile(priya)
    users.append(priya)
    print_success(f"Created: {priya.name} (Gig Worker, ₹25,000/month)")
    
    # User 3: Arjun - Student wanting to learn coding
    arjun = User(
        name="Arjun Reddy",
        phone="9876543212",
        date_of_birth=date(2000, 11, 8),
        state="Telangana",
        district="Hyderabad",
        employment_type=EmploymentType.STUDENT,
        monthly_income=0,
        kyc_status=KYCStatus.VERIFIED,
        kyc_verified_at=datetime.now(),
    )
    db.create_user(arjun)
    credit_identity_service.create_profile(arjun)
    users.append(arjun)
    print_success(f"Created: {arjun.name} (Student, seeking ISA for coding bootcamp)")
    
    # User 4: Lakshmi - Farmer
    lakshmi = User(
        name="Lakshmi Devi",
        phone="9876543213",
        date_of_birth=date(1978, 4, 12),
        state="Andhra Pradesh",
        district="Guntur",
        employment_type=EmploymentType.SELF_EMPLOYED,
        monthly_income=15000,
        kyc_status=KYCStatus.VERIFIED,
        kyc_verified_at=datetime.now(),
    )
    db.create_user(lakshmi)
    credit_identity_service.create_profile(lakshmi)
    users.append(lakshmi)
    print_success(f"Created: {lakshmi.name} (Farmer, needs crop insurance)")
    
    return users


def demo_earned_wage_access(user: User):
    """Demo EWA product with Ramesh"""
    print_header("💰 Demo 1: Earned Wage Access (EWA)")
    
    console.print(f"[bold]User:[/bold] {user.name}")
    console.print(f"[bold]Scenario:[/bold] Ramesh needs ₹5,000 for his mother's medicine.")
    console.print(f"[bold]Current income:[/bold] ₹{user.monthly_income}/month")
    console.print(f"[bold]Days into month:[/bold] {datetime.now().day}")
    console.print()
    
    simulate_delay()
    
    # Check eligibility
    print_info("Checking EWA eligibility...")
    eligibility = ewa_product.check_eligibility(user.id)
    
    table = Table(title="Eligibility Check")
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Eligible", "✓ Yes" if eligibility['eligible'] else "✗ No")
    table.add_row("Max Available", f"₹{eligibility.get('max_available', 0):,.0f}")
    table.add_row("Earned Wages (Est.)", f"₹{eligibility.get('earned_wages_estimate', 0):,.0f}")
    table.add_row("Processing Fee", f"{eligibility.get('processing_fee_rate', 0)*100:.1f}%")
    console.print(table)
    console.print()
    
    simulate_delay()
    
    # Request advance
    print_info("Requesting ₹5,000 advance...")
    request = ewa_product.request_advance(
        user_id=user.id,
        amount=5000,
        upi_vpa=f"{user.phone}@upi",
        express_disbursal=False
    )
    
    table = Table(title="EWA Request Approved")
    table.add_column("Detail", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Request ID", request.id[:8] + "...")
    table.add_row("Approved Amount", f"₹{request.approved_amount:,.0f}")
    table.add_row("Processing Fee", f"₹{request.processing_fee:,.0f}")
    table.add_row("Total Fee", f"₹{request.total_fee:,.0f}")
    table.add_row("Repayment Amount", f"₹{request.repayment_amount:,.0f}")
    table.add_row("Repayment Date", request.repayment_date.strftime("%d %b %Y"))
    console.print(table)
    console.print()
    
    simulate_delay()
    
    # Disburse
    print_info("Disbursing to UPI...")
    result = ewa_product.disburse_advance(request.id)
    print_success(f"₹{result['amount']:,.0f} sent to {user.phone}@upi")
    
    # Show stats
    stats = ewa_product.get_ewa_stats(user.id)
    console.print()
    console.print(f"[bold]Effective APR:[/bold] {stats['effective_apr']:.1f}% (vs 400%+ from moneylenders)")
    
    return request


def demo_income_share_agreement(user: User):
    """Demo ISA product with Arjun"""
    print_header("📚 Demo 2: Income Share Agreement (ISA)")
    
    console.print(f"[bold]User:[/bold] {user.name}")
    console.print(f"[bold]Scenario:[/bold] Arjun wants to join a 6-month coding bootcamp")
    console.print(f"[bold]Program cost:[/bold] ₹2,00,000")
    console.print(f"[bold]Current savings:[/bold] ₹0")
    console.print()
    
    simulate_delay()
    
    # Check eligibility
    print_info("Checking ISA eligibility...")
    eligibility = isa_product.check_eligibility(user.id, 200000)
    
    table = Table(title="ISA Eligibility & Terms")
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Eligible", "✓ Yes" if eligibility['eligible'] else "✗ No")
    table.add_row("Max Funding", f"₹{eligibility.get('max_funding', 0):,.0f}")
    table.add_row("Income Share", f"{eligibility.get('terms', {}).get('income_share_percentage', 0):.0f}%")
    table.add_row("Payment Duration", f"{eligibility.get('terms', {}).get('payment_duration_months', 0)} months")
    table.add_row("Min Income Threshold", f"₹{eligibility.get('terms', {}).get('minimum_income_threshold', 0):,.0f}/year")
    table.add_row("Payment Cap", f"₹{eligibility.get('terms', {}).get('payment_cap', 0):,.0f}")
    console.print(table)
    console.print()
    
    simulate_delay()
    
    # Simulate repayment at different incomes
    print_info("Simulating repayment at different income levels...")
    console.print()
    
    table = Table(title="ISA Repayment Scenarios")
    table.add_column("If Arjun Earns", style="cyan")
    table.add_column("Monthly Payment", style="yellow")
    table.add_column("Months to Complete", style="green")
    table.add_column("Total Paid", style="magenta")
    
    for income in [500000, 800000, 1200000, 1500000]:
        sim = isa_product.simulate_repayment_schedule(200000, income)
        table.add_row(
            f"₹{income:,}/year",
            f"₹{sim['monthly_payment']:,.0f}",
            f"{sim['estimated_months_to_complete']:.0f}",
            f"₹{sim['total_payments']:,.0f} ({sim['effective_cost_multiple']}x)"
        )
    
    console.print(table)
    console.print()
    
    simulate_delay()
    
    # Create contract
    print_info("Creating ISA contract...")
    contract = isa_product.create_contract(
        user_id=user.id,
        education_provider_id="bootcamp-001",
        education_provider_name="CodeMaster Academy",
        program_name="Full Stack Development Bootcamp",
        program_duration_months=6,
        education_cost=200000,
    )
    print_success(f"ISA Contract created: {contract.id[:8]}...")
    
    # Activate
    print_info("Activating contract (student enrolled)...")
    result = isa_product.activate_contract(contract.id, datetime.now())
    print_success(f"₹{result['funded_amount']:,.0f} disbursed to CodeMaster Academy")
    console.print()
    
    # Show timeline
    console.print("[bold]Timeline:[/bold]")
    console.print(f"  Program ends: {result['program_end_date'][:10]}")
    console.print(f"  Repayment starts: {result['repayment_start_date'][:10]} (after 3-month grace period)")
    
    return contract


def demo_parametric_insurance(user: User):
    """Demo parametric insurance with Lakshmi"""
    print_header("🌾 Demo 3: Parametric Crop Insurance")
    
    console.print(f"[bold]User:[/bold] {user.name}")
    console.print(f"[bold]Scenario:[/bold] Lakshmi wants protection against rainfall deficit")
    console.print(f"[bold]Location:[/bold] {user.district}, {user.state}")
    console.print(f"[bold]Coverage needed:[/bold] ₹1,00,000")
    console.print()
    
    simulate_delay()
    
    # Show available products
    print_info("Available insurance products...")
    products = parametric_insurance_product.get_available_products(user.state)
    
    table = Table(title="Available Parametric Insurance")
    table.add_column("Product", style="cyan")
    table.add_column("Trigger", style="yellow")
    table.add_column("Premium Rate", style="green")
    
    for p in products[:4]:
        table.add_row(
            p['name'],
            p['trigger'][:50] + "...",
            f"{p['premium_rate']*100:.1f}%"
        )
    console.print(table)
    console.print()
    
    simulate_delay()
    
    # Get quote
    print_info("Getting quote for Crop Rainfall Protection...")
    quote = parametric_insurance_product.calculate_premium(
        InsuranceType.CROP_RAINFALL,
        100000,
        12
    )
    
    table = Table(title="Insurance Quote")
    table.add_column("Detail", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Coverage Amount", f"₹{quote['coverage_amount']:,.0f}")
    table.add_row("Annual Premium", f"₹{quote['premium']:,.0f}")
    table.add_row("Monthly Premium", f"₹{quote['premium_per_month']:,.0f}")
    table.add_row("Duration", f"{quote['duration_months']} months")
    console.print(table)
    console.print()
    
    console.print("[bold]Payout Scenarios:[/bold]")
    for scenario in quote['payout_scenarios']:
        payout = scenario['payout']
        console.print(f"  • {scenario['scenario']}: ₹{payout:,.0f}")
    console.print()
    
    simulate_delay()
    
    # Purchase policy
    print_info("Purchasing policy...")
    policy = parametric_insurance_product.create_policy(
        user_id=user.id,
        insurance_type=InsuranceType.CROP_RAINFALL,
        coverage_amount=100000,
        coverage_location=user.district,
        state=user.state,
        payout_upi=f"{user.phone}@upi"
    )
    print_success(f"Policy created: {policy.id[:8]}...")
    
    # Activate
    print_info("Activating policy (premium paid)...")
    result = parametric_insurance_product.activate_policy(policy.id)
    print_success("Policy is now active!")
    console.print()
    
    # Simulate weather event
    print_warning("🌧️ SIMULATING WEATHER EVENT: Rainfall deficit of 25% in Guntur...")
    simulate_delay(1)
    
    results = parametric_insurance_product.simulate_weather_event(
        user.district,
        "rainfall_deficit_percentage",
        25  # 25% deficit
    )
    
    if results:
        console.print()
        console.print("[bold green]🎉 TRIGGER ACTIVATED![/bold green]")
        for r in results:
            console.print(f"[green]   ₹{r['payout_amount']:,.0f} instantly credited to {user.phone}@upi[/green]")
    
    return policy


def demo_credit_identity(users: list):
    """Demo credit identity building"""
    print_header("📊 Demo 4: Universal Credit Identity")
    
    console.print("[bold]Showing how alternative data builds credit scores...[/bold]")
    console.print()
    
    # Simulate UPI transactions for Priya (gig worker)
    priya = users[1]  # Gig worker
    
    print_info(f"Building credit score for {priya.name} from UPI data...")
    
    # Simulate 30 days of transactions
    transactions = [
        {'amount': 250, 'type': 'credit', 'timestamp': (datetime.now() - timedelta(days=i)).isoformat(), 'merchant': f'Swiggy_{i}'}
        for i in range(30)
    ] + [
        {'amount': 150, 'type': 'debit', 'timestamp': (datetime.now() - timedelta(days=i)).isoformat(), 'merchant': 'Grocery'}
        for i in range(20)
    ]
    
    profile = credit_identity_service.update_from_upi_data(priya.id, transactions)
    
    table = Table(title=f"Credit Profile: {priya.name}")
    table.add_column("Score Component", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Composite Score", f"{profile.composite_score} / 900")
    table.add_row("Payment History", f"{profile.payment_history_score}")
    table.add_row("Credit Utilization", f"{profile.credit_utilization_score}")
    table.add_row("Income Stability", f"{profile.income_stability_score}")
    table.add_row("Confidence Level", f"{profile.confidence_level*100:.0f}%")
    table.add_row("Data Sources", ", ".join(profile.data_sources))
    console.print(table)
    console.print()
    
    # Show credit decisions
    print_info("Credit decisions based on score...")
    
    table = Table(title="What Priya Can Access")
    table.add_column("Product", style="cyan")
    table.add_column("Limit", style="green")
    table.add_column("Rate", style="yellow")
    
    for product in ['ewa', 'personal_loan', 'credit_card']:
        decision = credit_identity_service.get_credit_decision(priya.id, product, 50000)
        if decision['approved']:
            table.add_row(
                product.upper().replace('_', ' '),
                f"₹{decision['max_amount']:,.0f}",
                f"{decision['interest_rate']*100:.1f}%"
            )
        else:
            table.add_row(product.upper().replace('_', ' '), "Not Eligible", "-")
    
    console.print(table)


def show_platform_summary():
    """Show final platform summary"""
    print_header("📈 Platform Summary")
    
    stats = db.get_stats()
    
    table = Table(title="India FinTech Platform Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Total Users", str(stats['total_users']))
    table.add_row("Credit Profiles", str(stats['credit_profiles']))
    table.add_row("Transactions", str(stats['transactions']))
    
    for product, count in stats.get('products', {}).items():
        table.add_row(f"Active {product.upper()}", str(count))
    
    console.print(table)
    console.print()
    
    # Show the vision
    console.print(Panel("""
[bold]🇮🇳 India FinTech Platform - Mission[/bold]

Building financial products that serve 1.4 billion Indians, not just the top 50 million.

[cyan]Products Demonstrated:[/cyan]
1. ✅ Earned Wage Access - Instant access to earned wages
2. ✅ Income Share Agreements - Pay for education from future earnings  
3. ✅ Parametric Insurance - Automatic payouts based on weather data

[cyan]Infrastructure Built:[/cyan]
• Universal Credit Identity - Credit scores for the unbanked
• Income Verification - Multi-source income validation
• Collection Infrastructure - UPI/NACH automated collections

[yellow]Total Addressable Impact:[/yellow]
• 300M Indians gaining credit access
• 450M with retirement savings
• 600M with adequate insurance
• 50M students able to afford education

[bold green]The debate is over. The work begins.[/bold green]
""", title="Vision", expand=False))


def main():
    """Run the complete demo"""
    console.print()
    console.print(Panel("""
[bold blue]🇮🇳 INDIA FINTECH PLATFORM[/bold blue]
[bold]Missing Financial Products for 1.4 Billion Indians[/bold]

Based on AI Agent Debate Analysis
""", expand=False))
    console.print()
    
    # Create users
    users = create_demo_users()
    simulate_delay(1)
    
    # Demo EWA with Ramesh
    demo_earned_wage_access(users[0])
    simulate_delay(1)
    
    # Demo ISA with Arjun
    demo_income_share_agreement(users[2])
    simulate_delay(1)
    
    # Demo Insurance with Lakshmi
    demo_parametric_insurance(users[3])
    simulate_delay(1)
    
    # Demo Credit Identity
    demo_credit_identity(users)
    simulate_delay(1)
    
    # Summary
    show_platform_summary()
    
    console.print()
    console.print("[bold green]Demo complete![/bold green]")
    console.print()
    console.print("To run the API server: [cyan]cd india_fintech_platform && python -m uvicorn api.main:app --reload[/cyan]")
    console.print("API docs will be at: [cyan]http://localhost:8000/docs[/cyan]")


if __name__ == "__main__":
    main()
