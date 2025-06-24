export const fetchMenu = async (restaurantId) => {
    return {
      sections: [
        {
          name: "Appetizers",
          items: [
            { id: 1, name: "Bruschetta", price: 5.99, dietary: "Vegetarian" },
            { id: 2, name: "Stuffed Mushrooms", price: 6.99, dietary: "Gluten-Free" },
          ],
        },
        {
          name: "Main Courses",
          items: [
            { id: 3, name: "Grilled Salmon", price: 14.99, dietary: "Pescatarian" },
            { id: 4, name: "Ribeye Steak", price: 18.99, dietary: "None" },
          ],
        },
      ],
    };
  };
  