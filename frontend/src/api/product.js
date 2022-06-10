import HTTP from "@/api/common";

export default {
  async topProducts() {
    const response = await HTTP.get("products/top_products/");
    return response;
  },
  async products_in_cart(params) {
    const response = await HTTP.get("products/products_in_cart/", {
      params: params,
      paramsSerializer: (params) => {
        return Object.entries(params)
          .map(([key, value]) => {
            if (Array.isArray(value)) {
              return value
                .map((value) => {
                  return `${key}=${value}`;
                })
                .join("&");
            }
            return `${key}=${value}`;
          })
          .join("&");
      },
    });
    return response;
  },
  async newProducts() {
    const response = await HTTP.get("products/new_products/");
    return response;
  },
  async detail(productId) {
    const response = await HTTP.get(`products/${productId}/`);
    return response;
  },
  async productCharacteristics(productId) {
    const response = await HTTP.get(`products/${productId}/characteristics/`);
    return response;
  },
  async productsReservedQuantity(productIds, startDate, endDate) {
    const response = await HTTP.get(`products/products_reserved_quantity/`, {
      params: {
        id: productIds,
        start_date: startDate,
        end_date: endDate,
      },
      paramsSerializer: (params) => {
        return Object.entries(params)
          .map(([key, value]) => {
            if (Array.isArray(value)) {
              return value
                .map((value) => {
                  return `${key}=${value}`;
                })
                .join("&");
            }
            return `${key}=${value}`;
          })
          .join("&");
      },
    });
    return response;
  },
};
