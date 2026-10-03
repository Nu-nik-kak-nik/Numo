pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir  = pkgdatadir / 'numo'
gnome      = import('gnome')

metainfo_dir = meson.project_build_root() / 'data'

gnome.compile_resources('numo',
  'numo.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
  source_dir: [
    '.',
    metainfo_dir,
    meson.current_source_dir(),
  ],
)

py = import('python').find_installation('python3')

conf = configuration_data()
conf.set('PYTHON', py.full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'numo.in',
  output: 'numo',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'rwxr-xr-x',
)

python_sources = {
  ''      : ['__init__.py', 'main.py'],
  'ui'    : [
    'ui/__init__.py',
    'ui/window.py',
    'ui/settings.py',
    'ui/statistics.py',
  ],
  'core'  : [
    'core/__init__.py',
    'core/core_settings.py',
    'core/stats_schema.py',
    'core/custom_errors.py',
    'core/settings_manager.py',
    'core/ui_constants.py',
  ],
  'utils' : [
    'utils/__init__.py',
    'utils/stats_manager.py',
  ],
  'game'  : [
    'game/__init__.py',
    'game/task.py',
    'game/task_generator.py',
    'game/game_session.py',
  ],
}

foreach sub, files : python_sources
  py.install_sources(
    files,
    pure: false,
    subdir: moduledir / sub,
  )
endforeach