const { spawnSync } = require('child_process');
var path = require('path')
var fs = require('fs');
const child = spawnSync('chp',
  ['generate', '--entry-point', 'webpack.entry.py'], {maxBuffer: 20000*1024}
);
fs.writeFile('webpack_bundle.py', child.stdout, function(err) {
  if(err) {
      return console.log(err);
  }
});

module.exports = {
  mode: 'development',
  entry: './webpack_bundle.py',
  output: {
    filename: 'todos.js',
    path: path.resolve(__dirname, 'todos/static')
  },
  module: {
    rules: [
      {
        test: /\.py$/,
        loader: 'py-loader',
        options: {
          compiler: 'transcrypt'
        }
      }
    ]
  }
}
