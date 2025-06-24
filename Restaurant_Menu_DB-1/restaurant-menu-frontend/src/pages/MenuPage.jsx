import { useEffect, useState } from "react";
import { fetchMenu } from "../services/api";

const MenuPage = () => {
  const [menu, setMenu] = useState({ sections: [] });
  const [filter, setFilter] = useState("");

  useEffect(() => {
    const getMenu = async () => {
      const data = await fetchMenu(1); // Mock restaurant ID
      setMenu(data);
    };
    getMenu();
  }, []);

  const filteredMenu = menu.sections.map((section) => ({
    ...section,
    items: section.items.filter((item) =>
      filter ? item.dietary.toLowerCase().includes(filter.toLowerCase()) : true
    ),
  }));

  return (
    <div className="bg-gray-50 min-h-screen">
      <header className="bg-blue-600 text-white py-6 shadow-md">
        <div className="container mx-auto px-6">
          <h1 className="text-4xl font-bold">Menu</h1>
          <p className="mt-2 text-blue-200">Explore menu items and filter by your preferences.</p>
        </div>
      </header>
  
      <main className="container mx-auto px-6 py-8">
        {/* Filter Dropdown */}
        <div className="mb-8">
          <label htmlFor="filter" className="block font-medium text-lg">Filter by Dietary Restriction:</label>
          <select
            id="filter"
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="mt-2 border rounded-lg p-2 w-full max-w-md"
          >
            <option value="">All</option>
            <option value="vegetarian">Vegetarian</option>
            <option value="gluten-free">Gluten-Free</option>
            <option value="pescatarian">Pescatarian</option>
            <option value="none">None</option>
          </select>
        </div>
  
        {/* Render Filtered Menu */}
        {filteredMenu.map((section) => (
          <div key={section.name} className="mb-10">
            <h2 className="text-2xl font-semibold border-b pb-2">{section.name}</h2>
            <ul className="mt-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {section.items.map((item) => (
                <li key={item.id} className="bg-white shadow-lg rounded-lg p-6">
                  <h3 className="text-lg font-semibold">{item.name}</h3>
                  <p className="text-gray-500 mt-2">${item.price.toFixed(2)}</p>
                  <span className="text-sm bg-blue-100 text-blue-700 px-2 py-1 rounded mt-4 inline-block">
                    {item.dietary}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </main>
    </div>
  );
};

export default MenuPage;
