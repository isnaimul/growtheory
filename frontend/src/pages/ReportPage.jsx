import React, { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import Navbar from "../components/layout/Navbar";
import ReportHeader from "../components/report/ReportHeader";
import ScoreCard from "../components/report/ScoreCard";
import MetricsGrid from "../components/report/MetricsGrid";
import VerdictCard from "../components/report/VerdictCard";
import InsightsList from "../components/report/InsightsList";
import DetailedAnalysis from "../components/report/DetailedAnalysis";
import apiService from "../services/api";

const ReportPage = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const ticker = searchParams.get("ticker");

  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!ticker) {
      navigate("/");
      return;
    }

    fetchReport();
  }, [ticker, navigate]);

  const fetchReport = async () => {
    try {
      setLoading(true);
      const data = await apiService.getReport(ticker);

      // Parse the full_analysis to extract structured data
      const parsedData = parseAnalysis(data);
      setReportData(parsedData);
    } catch (err) {
      console.error("Error fetching report:", err);
      setError("Failed to load report");
    } finally {
      setLoading(false);
    }
  };

  const parseAnalysis = (data) => {
    const analysis = data.full_analysis || "";

    console.log("=== RAW ANALYSIS TEXT ===");
    console.log(analysis);
    console.log("========================");

    // Extract green flags
    const greenFlagsMatch = analysis.match(
      /🟢 Green Flags:([\s\S]*?)(?=🔴|Market Sentiment|Recommendation|$)/
    );
    const greenFlags = greenFlagsMatch
      ? greenFlagsMatch[1]
          .split("\n")
          .filter((line) => line.trim().startsWith("-"))
          .map((line) => line.trim().substring(1).trim())
      : [];

    // Extract red flags
    const redFlagsMatch = analysis.match(
      /🔴 Potential Considerations:([\s\S]*?)(?=Market Sentiment|Recommendation|$)/
    );
    const redFlags = redFlagsMatch
      ? redFlagsMatch[1]
          .split("\n")
          .filter((line) => line.trim().startsWith("-"))
          .map((line) => line.trim().substring(1).trim())
      : [];

    // Extract recommendation
    const recommendationMatch = analysis.match(/Recommendation:\s*(.*)/);
    const recommendation = recommendationMatch
      ? recommendationMatch[1].trim()
      : "NEUTRAL ⚠️";

    // Extract financial data (from the full_analysis text)
    const revenueMatch = analysis.match(
      /Annual Revenue:\s*\$?([\d.]+)\s*(million|billion|trillion|M|B|T)/i
    );

    const marketCapMatch = analysis.match(
      /Market Cap:\s*\$?([\d.]+)\s*(million|billion|trillion|M|B|T)/i
    );
    const profitMarginMatch = analysis.match(/Profit Margin:\s*([\d.]+)%/i);

    const employeesMatch = analysis.match(/Total Employees:\s*([\d,]+)/i);
    const parseFinancialNumber = (match) => {
      if (!match) return null;
      const num = parseFloat(match[1].replace(/,/g, ""));
      const unit = match[2].toUpperCase();
      if (unit.startsWith("T")) return num * 1e12;
      if (unit.startsWith("B")) return num * 1e9;
      if (unit.startsWith("M")) return num * 1e6;
      return num;
    };

    return {
      company: data.company,
      ticker: data.ticker,
      score: data.score,
      grade: data.grade,
      timestamp: data.timestamp,
      recommendation: recommendation,
      greenFlags: greenFlags,
      redFlags: redFlags,
      financialData: {
        revenue: revenueMatch ? parseFinancialNumber(revenueMatch) : null,
        market_cap: marketCapMatch
          ? parseFinancialNumber(marketCapMatch)
          : null,
        profit_margin: profitMarginMatch
          ? parseFloat(profitMarginMatch[1])
          : null,
        employees: employeesMatch
          ? parseInt(employeesMatch[1].replace(/,/g, ""))
          : null,
      },
      detailedAnalysis: analysis,
    };
  };

  if (loading) {
    return (
      <>
        <Navbar showNewSearch={true} />
        <div className="report-container">
          <div className="container">
            <div className="loading-state">Loading report...</div>
          </div>
        </div>
      </>
    );
  }

  if (error || !reportData) {
    return (
      <>
        <Navbar showNewSearch={true} />
        <div className="report-container">
          <div className="container">
            <div className="error-state">{error || "Report not found"}</div>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <Navbar showNewSearch={true} />
      <div className="report-container">
        <div className="container">
          <ReportHeader
            companyName={reportData.company}
            ticker={reportData.ticker}
            timestamp={reportData.timestamp}
          />

          <ScoreCard score={reportData.score} grade={reportData.grade} />

          <VerdictCard verdict={reportData.recommendation} />

          <MetricsGrid financialData={reportData.financialData} />

          <InsightsList
            greenFlags={reportData.greenFlags}
            redFlags={reportData.redFlags}
          />

          <DetailedAnalysis detailedAnalysis={reportData.detailedAnalysis} />
        </div>
      </div>
    </>
  );
};

export default ReportPage;
