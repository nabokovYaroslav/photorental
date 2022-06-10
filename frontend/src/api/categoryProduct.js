import HTTP from "@/api/common";

export default {
  async list(categoryId, params, signal) {
    const response = await HTTP.get(`categories/${categoryId}/products/`, {
      params: params,
      signal: signal,
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
