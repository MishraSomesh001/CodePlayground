import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  allowedDevOrigins: ["http://192.168.1.44:3000"],
  turbopack: {
    root: process.cwd(),
  },
};

export default nextConfig;
