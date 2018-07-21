const { spawnSync } = require('child_process');
var fs = require('fs');
const child = spawnSync('chp', ['generate', '--entry-point', 'webpack.entry.py']);
fs.writeFile('webpack.bundle.py', child.output.join('\n'), function(err) {
  if(err) {
      return console.log(err);
  }
});

module.exports = {
    mode: 'development',
    entry: './webpack.bundle.py',
    output: {
      filename: 'lol.js',
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
