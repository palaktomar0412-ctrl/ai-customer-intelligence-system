"""
Report Generation routes - PDF and Excel report creation.
"""
import os
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import pandas as pd

from app.core.database import get_db
from app.core.config import settings
from app.models.models import Customer, Purchase, Report
from app.schemas.schemas import ReportCreate, ReportResponse, MessageResponse

router = APIRouter()


@router.get("", response_model=list[ReportResponse])
async def list_reports(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    report_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all generated reports."""
    query = select(Report).order_by(Report.created_at.desc())

    if report_type:
        query = query.where(Report.report_type == report_type)

    offset = (page - 1) * per_page
    query = query.offset(offset).limit(per_page)

    result = await db.execute(query)
    reports = result.scalars().all()

    return [ReportResponse.model_validate(r) for r in reports]


@router.post("/generate/customer-analytics", response_model=ReportResponse)
async def generate_customer_analytics_report(
    report_name: str = "Customer Analytics Report",
    file_format: str = "PDF",
    db: AsyncSession = Depends(get_db)
):
    """Generate a comprehensive customer analytics report."""
    # Create report record
    report = Report(
        report_name=report_name,
        report_type="Customer Analytics",
        file_format=file_format,
        status="Generating",
        generated_by=1,  # Default admin user
    )
    db.add(report)
    await db.flush()

    try:
        # Fetch customer data
        result = await db.execute(select(Customer))
        customers = result.scalars().all()

        if not customers:
            report.status = "Completed"
            return ReportResponse.model_validate(report)

        # Build data for report
        data = []
        for c in customers:
            data.append({
                "Customer ID": c.customer_id,
                "Name": f"{c.first_name} {c.last_name}",
                "Email": c.email,
                "Status": c.status,
                "Segment": c.segment,
                "Subscription": c.subscription_type,
                "Tenure (months)": c.tenure_months,
                "Monthly Charges": float(c.monthly_charges or 0),
                "Total Charges": float(c.total_charges or 0),
                "Churn Probability": float(c.churn_probability or 0),
                "Risk Level": c.risk_level,
                "CLV Score": float(c.clv_score or 0),
            })

        df = pd.DataFrame(data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"customer_analytics_{timestamp}"

        if file_format == "Excel":
            filepath = os.path.join(settings.REPORTS_DIR, f"{filename}.xlsx")
            os.makedirs(settings.REPORTS_DIR, exist_ok=True)

            with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name="Customer Analytics", index=False)

                # Summary sheet
                summary_data = {
                    "Metric": ["Total Customers", "Active", "Churned", "Avg Monthly Charges",
                               "Avg Total Charges", "Avg CLV Score"],
                    "Value": [
                        len(customers),
                        sum(1 for c in customers if c.status == "Active"),
                        sum(1 for c in customers if c.status == "Churned"),
                        round(df["Monthly Charges"].mean(), 2),
                        round(df["Total Charges"].mean(), 2),
                        round(df["CLV Score"].mean(), 2),
                    ]
                }
                pd.DataFrame(summary_data).to_excel(
                    writer, sheet_name="Summary", index=False
                )

            report.file_path = filepath
            report.file_format = "Excel"
        else:
            # PDF generation (simplified - uses reportlab in production)
            filepath = os.path.join(settings.REPORTS_DIR, f"{filename}.pdf")
            os.makedirs(settings.REPORTS_DIR, exist_ok=True)

            # Generate a text-based PDF placeholder
            # In production, use reportlab or weasyprint
            from fpdf import FPDF

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, txt="Customer Analytics Report", ln=True, align="C")
            pdf.set_font("Arial", "", 12)
            pdf.cell(200, 10, txt=f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
            pdf.ln(10)

            # Summary section
            pdf.set_font("Arial", "B", 14)
            pdf.cell(200, 10, txt="Summary", ln=True)
            pdf.set_font("Arial", "", 11)
            pdf.cell(200, 8, txt=f"Total Customers: {len(customers)}", ln=True)
            pdf.cell(200, 8, txt=f"Active: {sum(1 for c in customers if c.status == 'Active')}", ln=True)
            pdf.cell(200, 8, txt=f"Churned: {sum(1 for c in customers if c.status == 'Churned')}", ln=True)
            pdf.cell(200, 8, txt=f"Avg Monthly Charges: ${df['Monthly Charges'].mean():.2f}", ln=True)
            pdf.cell(200, 8, txt=f"Avg Total Charges: ${df['Total Charges'].mean():.2f}", ln=True)
            pdf.ln(10)

            # Customer table
            pdf.set_font("Arial", "B", 14)
            pdf.cell(200, 10, txt="Customer Details", ln=True)
            pdf.set_font("Arial", "", 9)

            for _, row in df.head(50).iterrows():  # Limit to 50 rows for PDF
                text = f"{row['Customer ID']} | {row['Name']} | {row['Status']} | {row['Segment']} | ${row['Total Charges']:.2f}"
                pdf.cell(200, 6, txt=text, ln=True)

            pdf.output(filepath)
            report.file_path = filepath
            report.file_format = "PDF"

        report.status = "Completed"
        report.completed_at = datetime.now()

    except Exception as e:
        report.status = "Failed"
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")

    return ReportResponse.model_validate(report)


@router.post("/generate/churn-analysis", response_model=ReportResponse)
async def generate_churn_report(
    report_name: str = "Churn Analysis Report",
    file_format: str = "PDF",
    db: AsyncSession = Depends(get_db)
):
    """Generate a churn analysis report."""
    report = Report(
        report_name=report_name,
        report_type="Churn Analysis",
        file_format=file_format,
        status="Generating",
        generated_by=1,
    )
    db.add(report)
    await db.flush()

    try:
        result = await db.execute(select(Customer))
        customers = result.scalars().all()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"churn_analysis_{timestamp}"
        filepath = os.path.join(settings.REPORTS_DIR, f"{filename}.xlsx")
        os.makedirs(settings.REPORTS_DIR, exist_ok=True)

        data = []
        for c in customers:
            data.append({
                "Customer ID": c.customer_id,
                "Name": f"{c.first_name} {c.last_name}",
                "Status": c.status,
                "Churn Probability": float(c.churn_probability or 0),
                "Risk Level": c.risk_level or "Unknown",
                "Tenure (months)": c.tenure_months,
                "Monthly Charges": float(c.monthly_charges or 0),
                "Complaints": c.complaints,
                "Support Tickets": c.support_tickets,
                "Usage Frequency": c.usage_frequency,
                "Segment": c.segment,
            })

        df = pd.DataFrame(data)

        with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Churn Analysis", index=False)

            # Risk distribution
            if not df.empty:
                risk_dist = df["Risk Level"].value_counts().to_dict()
                pd.DataFrame([
                    {"Risk Level": k, "Count": v}
                    for k, v in risk_dist.items()
                ]).to_excel(writer, sheet_name="Risk Distribution", index=False)

        report.file_path = filepath
        report.file_format = "Excel"
        report.status = "Completed"
        report.completed_at = datetime.now()

    except Exception as e:
        report.status = "Failed"
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")

    return ReportResponse.model_validate(report)


@router.get("/download/{report_id}")
async def download_report(report_id: int, db: AsyncSession = Depends(get_db)):
    """Download a generated report file."""
    result = await db.execute(select(Report).where(Report.id == report_id))
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if report.status != "Completed" or not report.file_path:
        raise HTTPException(status_code=400, detail="Report is not ready for download")

    if not os.path.exists(report.file_path):
        raise HTTPException(status_code=404, detail="Report file not found on disk")

    media_type = "application/pdf" if report.file_format == "PDF" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    return FileResponse(
        path=report.file_path,
        filename=f"{report.report_name.replace(' ', '_')}.{report.file_format.lower()}",
        media_type=media_type,
    )
