import React, { useState, useEffect } from "react";
import Table from "../components/Table";
import LoadingSpinner from "../components/LoadingSpinner";

const ReportsPage = () => {
  const [reportData, setReportData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulated API call to fetch report data
    const fetchReports = async () => {
      setIsLoading(true);

      // Mock data to simulate API response
      const mockData = [
        { category: "Appetizers", totalItems: 10, avgPrice: "$5.99" },
        { category: "Main Course", totalItems: 20, avgPrice: "$15.50" },
        { category: "Desserts", totalItems: 8, avgPrice: "$7.25" },
        { category: "Beverages", totalItems: 12, avgPrice: "$4.50" },
      ];

      setTimeout(() => {
        setReportData(mockData);
        setIsLoading(false);
      }, 1500); // Simulated delay
    };

    fetchReports();
  }, []);

  if (isLoading) {
    return (
      <div className="h-full flex justify-center items-center">
        <LoadingSpinner size="large" />
      </div>
    );
  }

  const columns = ["Category", "Total Items", "Average Price"];
  const data = reportData.map((item) => [item.category, item.totalItems, item.avgPrice]);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Reports</h1>
      <p className="text-gray-700 mb-6">
        Below is a summary of menu statistics, including the total number of items and average pricing by category.
      </p>
      <Table columns={columns} data={data} />
    </div>
  );
};

export default ReportsPage;
