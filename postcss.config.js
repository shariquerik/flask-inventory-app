module.exports = {
    plugins: [
      // ...
      require('tailwindcss'),
      require('autoprefixer'),
      require('@fullhuman/postcss-purgecss')({

        // Specify the paths to all of the template files in your project
        content: [
          './inventory/**/*.html'
          // etc.
        ],
      
        // This is the function used to extract class names from your templates
        defaultExtractor: content => content.match(/[A-Za-z0-9-_:]+/g) || []
        
        // {
        //   // Capture as liberally as possible, including things like `h-(screen-1.5)`
        //   const broadMatches = content.match(/[^<>"'`\s]*[^<>"'`\s:]/g) || []
      
        //   // Capture classes within other delimiters like .block(class="w-1/2") in Pug
        //   const innerMatches = content.match(/[^<>"'`\s.()]*[^<>"'`\s.():]/g) || []
      
        //   return broadMatches.concat(innerMatches)
        // }
      })
      // ...
    ]
  }