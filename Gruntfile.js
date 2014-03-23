module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    jshint: {
      src: ['www/js/main.js']
    },
    shell: {
      pythontests: {
        command: 'python setup.py test',
        options: {
          stdout: true,
          failOnError: true,
          execOptions: {
            cwd: 'webapp'
          }
        }
      }
    },
    clean: {
      staticTarget: ['<%= staticTarget %>'],
      wsgiTarget: ['<%= wsgiTarget %>']
    },
    copy: {
      staticTarget: {
        expand: true,
        cwd: 'www/',
        src: '**',
        dest: '<%= staticTarget %>/'
      },
      wsgiTarget: {
        expand: true,
        cwd: 'webapp/',
        src: '**',
        dest: '<%= wsgiTarget %>/'
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-shell');

  grunt.registerTask('forceOn', 'turns the --force option ON',
    function() {
      if ( !grunt.option( 'force' ) ) {
        grunt.config.set('forceStatus', true);
        grunt.option( 'force', true );
      }
    });

  grunt.registerTask('forceOff', 'turns the --force option Off',
    function() {
      if ( grunt.config.get('forceStatus') ) {
        grunt.option( 'force', false );
      }
    });

  grunt.registerTask('deploy',
    'Deploy to the target locations --wsgi-target and --static-target.',
    function() {
      var dirs = {
        wsgiTarget: grunt.option('wsgiTarget'),
        staticTarget: grunt.option('staticTarget')
      };

      for( var key in dirs ) {
        var dir = dirs[key];
        if( !(typeof dir == 'string' || dir instanceof String ) || !grunt.file.exists(dir) || !grunt.file.isDir(dir) ) {
          grunt.fail.fatal(key + ' must be a directory that exists');
        }
        grunt.config.set(key, dir);
      }
      grunt.task.run(['check', 'forceOn', 'clean', 'forceOff', 'copy']);
    }
  );

  grunt.registerTask('check', ['jshint', 'shell:pythontests']);

  grunt.registerTask('default', function() {
    grunt.log.writeln('Usage: \'check\' or \'deploy\'.');
  });

};
