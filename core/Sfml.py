#!/usr/bin/env python
# Author O Wasalski 
# OW - 07/06/2012 <wasalski@berkeley.edu> : First revision, new file
# The SFML packages base class
# Currently assumes all dependencies are installed on host machines
import LocalPackage
import os
import PackageUtil

def Snoingall(iterable):
    """ New in python 2.5, we target 2.4-tis annoying."""
    for element in iterable:
        if not element:
            return False
    return True

class Sfml( LocalPackage.LocalPackage ):
    """ Base sfml installer package."""

    def __init__( self, name, revision = "" ):
        """ Initialise sfml with the tarName."""
        super( Sfml, self ).__init__( name )
        if( revision == "" ):
            revision = "master"
        self._URL = "https://github.com/LaurentGomila/SFML/tarball/" + revision
        self._TarName = self._Name + ".tar.gz"
        return

########### "Public" functions - overrides LocalPackage ################

    def CheckState( self ):
        """ Check if downloaded and installed."""
        self._SetMode( 0 )
        if( self._Downloaded() ):
            self._SetMode( 1 )
        if( self._Installed() ):
            self._SetMode( 2 )

    def GetDependencies( self ):
        """ Return the required dependencies."""
        return ["cmake", "pthread", "opengl", "xlib", "xrandr", "freetype", "glew", "jpeg", "sndfile", "openal"]

########### "Private" functions - overrides LocalPackage ################

    def _Download( self ):
        """ Derived classes should override this to download the package. 
        Return True on success.""" 
        PackageUtil.DownloadFile( self._URL, fileName = self._TarName )
        return self._Downloaded()

    def _Install( self ):
        """ Install the version."""
        env = os.environ
        installPath = self.GetInstallPath()
        PackageUtil.UnTarFile( self._TarName, installPath, 1 )

        if self._DependencyPaths["cmake"] is not None: # Special cmake installed
            self._InstallPipe += PackageUtil.ExecuteSimpleCommand( "%s/bin/cmake" % self._DependencyPaths["cmake"], [ "-DCMAKE_INSTALL_PREFIX:PATH=$PWD" ], env, installPath ) 
        else:
            self._InstallPipe += PackageUtil.ExecuteSimpleCommand( "cmake", [ "-DCMAKE_INSTALL_PREFIX:PATH=$PWD" ], env, installPath ) 
        PackageUtil.ExecuteSimpleCommand( "make", [], env, installPath )
        return self._Installed()

########### "Private" functions - helper for this class only ################

    def _Downloaded( self ):
        tarball = os.path.join( PackageUtil.kCachePath, self._TarName )
        return os.path.isfile( tarball )

    def _Installed( self ):
        libDir = os.path.join( self.GetInstallPath(), "lib" )
        libs = [ "audio", "graphics", "network", "system", "window" ]
        libPaths = [ libDir + "/libsfml-" + lib + ".so" for lib in libs ]
        return Snoingall( [ os.path.isfile( libPath ) for libPath in libPaths ] )


