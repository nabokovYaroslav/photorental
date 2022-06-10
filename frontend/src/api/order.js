import HTTP from "@/api/common";

export default {
  async create(surname, name, phone, startDate, endDate, products) {
    const response = await HTTP.post("orders/", {
      surname: surname,
      name: name,
      phone: phone,
      start_date: startDate,
      end_date: endDate,
      products_in_order: products,
    });
    return response;
  },
};
