var path = require('path')
var webpack = require('webpack')
var HtmlWebpackPlugin = require('html-webpack-plugin')
var HtmlWebpackInlineSourcePlugin = require('html-webpack-inline-source-plugin')
var CopyWebpackPlugin = require('copy-webpack-plugin')

module.exports = {
  entry: './src/main.js',
  output: {
    path: path.resolve(__dirname, './dist'),
    publicPath: process.env.NODE_ENV === 'production'
                  ? './'
                  : '/',
    filename: '[name].js'
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: {
          loaders: {
            'scss': 'vue-style-loader!css-loader!sass-loader',
            'sass': 'vue-style-loader!css-loader!sass-loader?indentedSyntax'
          }
        }
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/
      }
    ]
  },
  resolve: {
    extensions: ['.js', '.vue', '.json'],
    alias: {
      'vue$': 'vue/dist/vue.esm.js',
      '@': path.resolve(__dirname, 'src')
    }
  },
  plugins: [
    new HtmlWebpackPlugin({
      inlineSource: '.js',
      filename: 'template.html',
      template: './src/template.html'
    }),
    new HtmlWebpackPlugin({
      inlineSource: '.js',
      filename: 'results.html',
      template: './src/results.html'
    }),
    new HtmlWebpackPlugin({
      inlineSource: '.js',
      filename: 'tutorial.html',
      template: './src/tutorial.html'
    }),
    new HtmlWebpackInlineSourcePlugin(),
    new CopyWebpackPlugin([
        { from: 'config/long_description.md' }
    ]),

  ]
}

console.log(JSON.stringify(require('./dist/project.json').short_name))

if (process.env.NODE_ENV === 'development') {
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"development"',
        SHORT_NAME: JSON.stringify(require('./dist/project.json').short_name)
      }
    })
  ])
}

if (process.env.NODE_ENV === 'production') {
  // http://vue-loader.vuejs.org/en/workflow/production.html
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"production"',
        SHORT_NAME: JSON.stringify(require('./dist/project.json').short_name)
      }
    }),
    new webpack.optimize.UglifyJsPlugin({
      compress: {
        warnings: false
      }
    })
  ])
}