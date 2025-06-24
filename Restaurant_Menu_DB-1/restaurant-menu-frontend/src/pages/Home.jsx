import React from "react";
import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div className="h-full bg-gradient-to-r from-blue-500 via-blue-600 to-blue-700 text-white">
      {/* Hero Section */}
      <div className="flex flex-col items-center justify-center h-96 bg-cover bg-center bg-opacity-90 p-6">
        <h1 className="text-5xl font-bold mb-4">Welcome to Menu Management</h1>
        <p className="text-xl text-center mb-6 max-w-3xl">
          Streamline restaurant menu management with AI-powered tools. Upload PDFs, manage menus, and generate insightful reports effortlessly.
        </p>
        <Link
          to="/menu"
          className="bg-white text-blue-700 px-6 py-3 rounded-lg shadow-md font-semibold hover:bg-gray-200 transition"
        >
          Get Started
        </Link>
      </div>

      {/* Feature Section */}
      <div className="p-8 bg-gray-100 text-gray-800">
        <h2 className="text-3xl font-bold text-center mb-8">Features</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Feature Card: View Menus */}
          <div className="bg-white rounded-lg shadow-lg p-6 text-center hover:shadow-xl transition">
            <div className="text-blue-600 text-4xl mb-4">
              <i className="fas fa-utensils"></i>
            </div>
            <h3 className="text-xl font-semibold mb-2">View Menus</h3>
            <p className="text-gray-600 mb-4">
              Explore restaurant menus, filter by dietary restrictions, and view detailed pricing.
            </p>
            <Link
              to="/menu"
              className="text-blue-600 font-semibold hover:underline"
            >
              Vamos!
            </Link>
          </div>

          {/* Feature Card: Manage Menus */}
          <div className="bg-white rounded-lg shadow-lg p-6 text-center hover:shadow-xl transition">
            <div className="text-green-600 text-4xl mb-4">
              <i className="fas fa-edit"></i>
            </div>
            <h3 className="text-xl font-semibold mb-2">Manage Menus</h3>
            <p className="text-gray-600 mb-4">
              Upload new menus, edit menu items, and organize sections easily.
            </p>
            <Link
              to="/admin"
              className="text-green-600 font-semibold hover:underline"
            >
              Vamos!
            </Link>
          </div>

          {/* Feature Card: Generate Reports */}
          <div className="bg-white rounded-lg shadow-lg p-6 text-center hover:shadow-xl transition">
            <div className="text-red-600 text-4xl mb-4">
              <i className="fas fa-chart-line"></i>
            </div>
            <h3 className="text-xl font-semibold mb-2">Generate Reports</h3>
            <p className="text-gray-600 mb-4">
              Get detailed insights and reports on menu performance and pricing trends.
            </p>
            <Link
              to="/reports"
              className="text-red-600 font-semibold hover:underline"
            >
              Vamos!
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
