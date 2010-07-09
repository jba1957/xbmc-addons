"""
    Category module: fetches a list of genres to use as folders
"""

# main imports
import sys
import os
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

from pysqlite2 import dbapi2 as sqlite


_ = xbmcaddon.Addon( id="plugin.video.apple.movie.trailers" ).getLocalizedString
_S = xbmcaddon.Addon( id="plugin.video.apple.movie.trailers" ).getSetting

class Main:
    # base paths
    BASE_SKIN_THUMBNAIL_PATH = os.path.join( xbmc.translatePath( "special://skin/" ), "media", sys.modules[ "__main__" ].__plugin__ )
    print BASE_SKIN_THUMBNAIL_PATH
    # TODO: remove all references
    #BASE_PLUGIN_THUMBNAIL_PATH = os.path.join( sys.modules[ "__main__" ].BASE_PATH, "thumbnails" )

    def __init__( self ):
        # if no database was found we need to run the script to create it.
        if ( not os.path.isfile( _S( "amt_db_path" ) ) ):
            self._launch_script()
        else:
            self.get_categories()

    def _launch_script( self ):
        # we need to get the localized strings before the call to endOfDirectory()
        msg1 = _( 30600 )
        msg2 = _( 30601 )
        msg3 = _( 30602 )
        # no database was found so notify XBMC we're finished, false so no blank list is shown
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=False )
        # we use "U:\\" for linux, windows and osx for platform mode
        drive = xbmc.translatePath( "special://home/" )
        # ask to run script to create the database
        if ( os.path.isfile( os.path.join( drive, "scripts", sys.modules[ "__main__" ].__script__, "addon.py" ) ) ):
            if ( xbmcgui.Dialog().yesno( sys.modules[ "__main__" ].__plugin__, msg1, msg3 ) ):
                xbmc.executebuiltin( "XBMC.RunScript(%s)" % ( os.path.join( drive, "scripts", sys.modules[ "__main__" ].__script__, "addon.py" ) ), )
        else:
            ok = xbmcgui.Dialog().ok( sys.modules[ "__main__" ].__plugin__, msg1, msg2, sys.modules[ "__main__" ].__svn_url__ )

    def get_categories( self ):
        try:
            # fetch genres from database
            genres = self._fetch_records()
            # add search category
            genres += [ ( -99, _( 30900 ), 0, 0, "", ) ]
            # fill media list
            self._fill_media_list( genres )
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )

    def _fill_media_list( self, genres ):
        try:
            ok = True
            # enumerate through the list of genres and add the item to the media list
            for genre in genres:
                url = "%s?genre_id=%d&genre=%s" % ( sys.argv[ 0 ], genre[ 0 ], repr( genre[ 1 ] ), )
                # check for a valid custom thumbnail for the current category
                thumbnail = self._get_thumbnail( genre[ 1 ] )
                # set the default icon
                icon = "DefaultFolder.png"
                # only need to add label, icon and thumbnail, setInfo() and addSortMethod() takes care of label2
                listitem=xbmcgui.ListItem( genre[ 1 ], iconImage=icon, thumbnailImage=thumbnail )#, "(%d)" % genre[ 2 ] )
                # add the different infolabels we want to sort by
                listitem.setInfo( type="Video", infoLabels={ "Date": "%s-%s-%s" % ( genre[ 4 ][ 8 : ], genre[ 4 ][ 5 : 7 ], genre[ 4 ][ : 4 ], ) } )
                # add the item to the media list
                ok = xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=url, listitem=listitem, isFolder=True, totalItems=len(genres) )
                if ( not ok ): raise
        except:
            # user cancelled dialog or an error occurred
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            ok = False
        # if successful and user did not cancel, set our sort orders, content and fanart
        if ( ok ):
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
            # set content
            xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="movies" )
            try:
                # set our fanart from user setting
                if ( _S( "fanart_genre" ) == "true" ):
                    if ( _S( "fanart_genre_path" ) ):
                        image_path = os.path.join( _S( "fanart_genre_path" ), "Genres.tbn" )
                        if ( os.path.isfile ( image_path ) ):
                            xbmcplugin.setPluginFanart( handle=int( sys.argv[ 1 ] ), image=image_path, color1=_S( "fanart_color1" ), color2=_S( "fanart_color2" ), color3=_S( "fanart_color3" ) )
                elif ( _S( "fanart_image" ) ):
                    xbmcplugin.setPluginFanart( handle=int( sys.argv[ 1 ] ), image=_S( "fanart_image" ), color1=_S( "fanart_color1" ), color2=_S( "fanart_color2" ), color3=_S( "fanart_color3" ) )
            except:
                pass
        # send notification we're finished, successfully or unsuccessfully
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=ok )

    def _get_thumbnail( self, title ):
        # create the full thumbnail path for skins directory
        thumbnail = os.path.join( self.BASE_SKIN_THUMBNAIL_PATH, title.replace( "*", "" ) + ".tbn" )
        # use a plugin custom thumbnail if a custom skin thumbnail does not exists
        if ( not os.path.isfile( thumbnail ) ):
            # TODO: remove this block (no plans on supplying thumbnails)
            # create the full thumbnail path for plugin directory
            #thumbnail = xbmc.translatePath( os.path.join( self.BASE_PLUGIN_THUMBNAIL_PATH, title.replace( "*", "" ) + ".tbn" ) )
            # use a default thumbnail if a custom thumbnail does not exists
            #if ( not os.path.isfile( thumbnail ) ):
            thumbnail = ""
        return thumbnail

    def _fetch_records( self ):
        records = Records( amt_db_path=xbmc.translatePath( _S( "amt_db_path" ) ) )
        result = records.fetch( Query()[ "genres" ] )
        records.close()
        return result


class Records:
    def __init__( self, *args, **kwargs ):
        self.connect( kwargs[ "amt_db_path" ] )

    def connect( self, db ):
        self.db = sqlite.connect( db )
        self.cursor = self.db.cursor()
    
    def close( self ):
        self.db.close()
    
    def fetch( self, sql, params=None ):
        try:
            if ( params is not None ): self.cursor.execute( sql, params )
            else: self.cursor.execute( sql )
            retval = self.cursor.fetchall()
        except:
            retval = None
        return retval


class Query( dict ):
	def __init__( self ):
		self[ "genres" ] = """	
									SELECT genres.idGenre, genres.genre, count(genre_link_movie.idGenre), count(movies.favorite), genres.updated 
									FROM genre_link_movie, genres, movies 
									WHERE genre_link_movie.idGenre=genres.idGenre 
									AND genre_link_movie.idMovie=movies.idMovie 
									GROUP BY genres.genre;
								"""
