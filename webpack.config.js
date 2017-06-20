'use strict';

const webpack = require('webpack');
const path = require('path');

module.exports = {
  entry: {
    main: "./src/js/main.js"
  },
  output: {
    path: path.resolve("./dist"),
    filename: "bundle.js"
  },
  module: {
    loaders: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: 'babel-loader'
      }
    ]
  }
};
