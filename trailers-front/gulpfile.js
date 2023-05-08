const gulp = require('gulp')
const strip = require('gulp-strip-comments')
const sass = require('gulp-sass')
const browserSync = require('browser-sync').create()
const nunjucksRender = require('gulp-nunjucks-render')
const prettify = require('gulp-jsbeautifier')
const plumber = require('gulp-plumber')
const concat = require('gulp-concat')
const uglify = require('gulp-uglify-es').default
const cleanCSS = require('gulp-clean-css')
const rename = require('gulp-rename')
const imagemin = require('gulp-imagemin')
const autoprefixer = require('gulp-autoprefixer')
const sourcemaps = require('gulp-sourcemaps')
const webpackStream = require('webpack-stream')
const webp = require('gulp-webp')
const named = require('vinyl-named')

gulp.task('browser-sync', () => {
  browserSync.init({
    server: {
      baseDir: './dist'
    },
    notify: false
  })
})

gulp.task('nunjucks', () => {
  return gulp
    .src('src/pages/**/*.njk')
    .pipe(plumber())
    .pipe(
      nunjucksRender({
        path: ['src/templates/']
      })
    )
    .pipe(
      prettify({
        indent_size: 4,
        preserve_newlines: true,
        max_preserve_newlines: 0
      })
    )
    .pipe(gulp.dest('dist'))
    .on('end', browserSync.reload)
})

gulp.task('sass', () => {
  return gulp
    .src([
      './src/scss/fonts.scss',
      './src/scss/inline.scss',
      './src/scss/style.scss',
      './src/scss/vendor.scss'
    ])
    .pipe(
      sass({
        outputStyle: 'compressed'
      }).on('error', sass.logError)
    )
    .pipe(
      autoprefixer({
        overrideBrowserslist: ['last 2 versions', '> 0.9%', 'not dead']
      })
    )
    .pipe(cleanCSS())
    .pipe(
      rename({
        suffix: '.min'
      })
    )
    .pipe(gulp.dest('../trailersplus/trailersplus/static/css'))
})

gulp.task('js', () => {
  return gulp
    .src([
      'src/js/script.js',
      'src/js/checkout.js',
      'src/js/product-page.js',
      'src/js/category-filter.js',
      'src/js/product-reviews.js'
    ])
    .pipe(named())
    .pipe(
      webpackStream({
        mode: 'production',
        // output: {
        // 	filename: 'script.min.js',
        // },
        module: {
          rules: [
            {
              test: /\.m?js$/,
              exclude: /(node_modules|bower_components)/,
              use: {
                loader: 'babel-loader',
                options: {
                  presets: ['@babel/preset-env'],
                  plugins: [
                    [
                      '@babel/plugin-transform-runtime',
                      {
                        absoluteRuntime: false,
                        corejs: false,
                        helpers: true,
                        regenerator: true,
                        useESModules: false,
                        version: '7.0.0-beta.0'
                      }
                    ]
                  ]
                }
              }
            }
          ]
        }
      })
    )
    .pipe(uglify())
    .pipe(strip())
    .pipe(gulp.dest('../trailersplus/trailersplus/static/js'))
    .pipe(browserSync.stream())
})

gulp.task('libs', () => {
  return gulp
    .src([
      'src/js/libs/magnific-popup.min.js',
      'src/js/libs/select2.min.js',
      'src/js/libs/swiper.min.js',
      'src/js/libs/tempus-dominus.min.js'
    ])
    .pipe(concat('libs.min.js'))
    .pipe(uglify())
    .pipe(strip())
    .pipe(gulp.dest('../trailersplus/trailersplus/static/js'))
    .pipe(browserSync.stream())
})

gulp.task('imagemin', () => {
  return gulp.src('src/img/**/*').pipe(imagemin()).pipe(gulp.dest('dist/img'))
})

gulp.task('webp', () =>
  gulp
    .src(['src/img/**/*.jpg', 'src/img/**/*.png'])
    .pipe(webp({ quality: 90 }))
    .pipe(gulp.dest('./dist/img/webp'))
)

gulp.task('build', gulp.series('sass', 'js', 'nunjucks'))

gulp.task('watch', () => {
  gulp.watch('src/scss/**/*.scss', gulp.parallel('sass'))
  gulp.watch(['src/libs/**/*.js', 'src/js/**/*.js'], gulp.parallel('js'))
  gulp.watch(
    ['src/pages/**/*.njk', 'src/templates/**/*.njk'],
    gulp.parallel('nunjucks')
  )
})

gulp.task('assets', gulp.parallel('sass', 'js', 'libs'))
gulp.task('default', gulp.parallel('sass', 'js', 'browser-sync', 'watch'))
