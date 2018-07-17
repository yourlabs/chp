module.exports = {
    mode: 'development',
    entry: './chp_build.py',
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
