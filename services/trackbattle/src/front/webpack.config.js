const path = require("path");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");
const HtmlMinifierPlugin = require("html-minifier-webpack-plugin");
const HtmlWebpackPlugin = require("html-webpack-plugin");

const src = path.resolve(__dirname, "src");

module.exports = {
    mode: process.env.NODE_ENV === "production" ? "production" : "development",
    entry: ["./src/index.tsx"],
    output: {
        path: path.resolve(__dirname, "build"),
        filename: "bundle.[hash].js",
        publicPath: process.env.NODE_ENV === "production" ? "/" : "http://localhost:5000/",
    },
    module: {
        rules: [
            {
                test: /\.(ts|tsx)$/,
                include: src,
                loader: "ts-loader",
            },
            {
                test: /\.less$/,
                include: src,
                use: [
                    "style-loader",
                    {
                        loader: "css-loader",
                        options: {
                            modules: {
                                localIdentName: process.env.NODE_ENV === "production" ? "[hash:base64]" : "[local]-[hash:base64]",
                                mode: "local",
                            },
                            esModule: false,
                        },
                    },
                    {
                        loader: "less-loader",
                        options: {
                            lessOptions: {
                                paths: [path.resolve(__dirname)],
                            },
                        },
                    },
                ],
            },
        ],
    },
    plugins: [
        new CleanWebpackPlugin(),
        new HtmlWebpackPlugin({
            template: 'public/index.html',
        })
    ],
    optimization: {
        minimizer: [
            new TerserPlugin(),
            new HtmlMinifierPlugin()
        ]
    },
    resolve: {
        extensions: [".ts", ".tsx", ".js", ".jsx"],
        modules: ["node_modules"],
    },
    devServer: {
        host: "0.0.0.0",
        port: 5000,
        proxy: {
            '/api': {
                target: {
                    host: "0.0.0.0",
                    protocol: 'http:',
                    port: 8080
                },
                pathRewrite: {
                    '^/api': '/api'
                }
            }
        },
    }
}