const mix = require('laravel-mix');

/*
 |--------------------------------------------------------------------------
 | Mix Asset Management
 |--------------------------------------------------------------------------
 |
 */

mix.js('resources/js/app.js', 'public/js')
   .sass('resources/scss/app.scss', 'public/css')
   .sass('resources/scss/style.scss', 'public/css')
   .sass('resources/scss/core/betting.scss', 'public/css/core')
   .sass('resources/scss/core/profile.scss', 'public/css/core')
   .sass('resources/scss/core/resulting.scss', 'public/css/core')
   .sass('resources/scss/core/faq.scss', 'public/css/core')
   .sass('resources/scss/core/account.scss', 'public/css/core');
