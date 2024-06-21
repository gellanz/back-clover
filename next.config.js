/** @type {import('next').NextConfig} */
const nextConfig = {
    rewrites: async () => {
      return [
        {
          source: "/:path*",
          destination:
            process.env.NODE_ENV === "development"
              ? "http://0.0.0.0:8000/:path*"
              : "/",
        },
        {
          source: "/docs",
          destination:
            process.env.NODE_ENV === "development"
              ? "http://0.0.0.0:8000/docs"
              : "/docs",
        },
        {
          source: "/openapi.json",
          destination:
            process.env.NODE_ENV === "development"
              ? "http://0.0.0.0:8000/openapi.json"
              : "/openapi.json",
        },
      ];
    },
  };
  
  module.exports = nextConfig;