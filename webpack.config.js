var webpack = require('webpack');
var path = require('path');
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var HtmlWebpackPlugin = require('html-webpack-plugin');
var BowerWebpackPlugin = require('bower-webpack-plugin');

var BUILD_DIR = path.resolve(__dirname, 'app/resources/public');
var APP_DIR = path.resolve(__dirname, 'app/resources/src');

module.exports = function (env) {
  const nodeEnv = env && env.prod ? 'production' : 'development';
  const isProd = nodeEnv === 'production';

  console.log("Loading webpack config for " + nodeEnv);

  var plugins = [
    new webpack.EnvironmentPlugin({
      NODE_ENV: nodeEnv,
    }),
    new HtmlWebpackPlugin({
      template: APP_DIR + '/index.template.ejs',
      inject: 'body',
    }),
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
      'window.jQuery': 'jquery'
    }),
    new ExtractTextPlugin("[name].css?[hash:20]"),
    new webpack.optimize.CommonsChunkPlugin({
      name: 'vendor',
      minChunks: function (module) {
        // this assumes your vendor imports exist in the node_modules directory
        return module.context && module.context.indexOf('node_modules') !== -1;
      }
    }),
    //CommonChunksPlugin will now extract all the common modules from vendor and main bundles
    new webpack.optimize.CommonsChunkPlugin({
      name: 'manifest' //But since there are no more common modules between them we end up with just the runtime code included in the manifest file
    })
  ];

  if (isProd) {
    console.log("Setting up Production Plugins");
    plugins.push(
      new webpack.LoaderOptionsPlugin({
        minimize: true,
        debug: false
      }),
      new webpack.optimize.UglifyJsPlugin({
        compress: {
          warnings: false,
          screw_ie8: true,
          conditionals: true,
          unused: true,
          comparisons: true,
          sequences: true,
          dead_code: true,
          evaluate: true,
          if_return: true,
          join_vars: true,
        },
        output: {
          comments: false,
        },
      })
    );
  } else {
    plugins.push(
      new webpack.HotModuleReplacementPlugin()
    );
  }

  var config = {
    devtool: isProd ? 'source-map' : 'eval',
    entry: {
      app: APP_DIR + '/app.jsx',
    },
    output: {
      path: BUILD_DIR,
      filename: '[name].[hash].js',
      publicPath: "/"
    },
    module: {
      rules: [
        {
          test: /\.jsx?/,
          include: APP_DIR,
          loader: 'babel-loader',
          options: {
            presets: [
              ['es2015'],
              ["react"]
            ]
          }
        },
        {
          test: /\.css$/,
          loader: ExtractTextPlugin.extract({ fallback: "style-loader", use: "css-loader" })
        },
        { test: /\.(woff|svg|ttf|eot|woff2)([\?]?.*)$/, loader: "file-loader?name=[name].[hash:20].[ext]" },
        { test: /\.(scss|less)$/, loader: ExtractTextPlugin.extract({ fallback: 'style-loader', use: 'css-loader!less-loader?indentedSyntax=true&sourceMap=true' }) },
        {
          test: /\.json$/,
          loader: "json-loader"
        },
        {
          test: /\.(png|jpg|gif)$/,
          loader: 'file-loader?name=[name].[hash:20].[ext]'
        }
      ]
    },
    plugins: plugins,
  };

  config['devServer'] = {
    port: 4000,
    host: "0.0.0.0",
    publicPath: config.output.publicPath,
    historyApiFallback: true,
    compress: isProd,
    inline: !isProd,
    hot: !isProd,
    proxy: {
      '/api/*': 'http://127.0.0.1:5000'
    },
    stats: {
      assets: true,
      children: false,
      chunks: false,
      hash: false,
      modules: false,
      publicPath: false,
      timings: true,
      version: false,
      warnings: true,
      colors: {
        green: '\u001b[32m',
      }
    },
  }

  return config;
}
