export default {
  base: "./",
  build: {
    lib: {
      entry: "./src/main.js",
      name: "trame_flow",
      formats: ["umd"],
      fileName: "trame_flow",
    },
    rollupOptions: {
      external: ["vue"],
      output: {
        globals: {
          vue: "Vue",
        },
      },
    },
    outDir: "../src/trame_flow/module/serve",
    assetsDir: ".",
  },
  define: {
    "process.env": { NODE_ENV: "production" },
  },
};
