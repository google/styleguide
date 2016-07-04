/*****************************************************************************
 * libvlc.c: libvlc instances creation and deletion, interfaces handling
 *****************************************************************************
 * Copyright (C) 1998-2008 VLC authors and VideoLAN
 * $Id: 3468e0e5b2ef424ac53c2ad6b69d2a3f8382cd28 $
 *
 * Authors: Vincent Seguin <seguin@via.ecp.fr>
 *          Samuel Hocevar <sam@zoy.org>
 *          Gildas Bazin <gbazin@videolan.org>
 *          Derk-Jan Hartman <hartman at videolan dot org>
 *          Rémi Denis-Courmont <rem # videolan : org>
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation; either version 2.1 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program; if not, write to the Free Software Foundation,
 * Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
 *****************************************************************************/

/** \file
 * This file contains functions to create and destroy libvlc instances
 */

/*****************************************************************************
 * Preamble
 *****************************************************************************/
#ifdef HAVE_CONFIG_H
# include "config.h"
#endif

#include <vlc_common.h>
#include "../lib/libvlc_internal.h"
#include <vlc_input.h>

#include "modules/modules.h"
#include "config/configuration.h"
#include "playlist/preparser.h"

#include <stdio.h>                                              /* sprintf() */
#include <string.h>
#include <stdlib.h>                                                /* free() */
#include <errno.h>

#include "config/vlc_getopt.h"

#ifdef HAVE_DBUS
/* used for one-instance mode */
#   include <dbus/dbus.h>
#endif


#include <vlc_playlist.h>
#include <vlc_interface.h>

#include <vlc_charset.h>
#include <vlc_dialog.h>
#include <vlc_keystore.h>
#include <vlc_fs.h>
#include <vlc_cpu.h>
#include <vlc_url.h>
#include <vlc_modules.h>

#include "libvlc.h"
#include "playlist/playlist_internal.h"
#include "misc/variables.h"

#include <vlc_vlm.h>

#ifdef __APPLE__
# include <libkern/OSAtomic.h>
#endif

#include <assert.h>

/*****************************************************************************
 * Local prototypes
 *****************************************************************************/
static void GetFilenames  ( libvlc_int_t *, unsigned, const char *const [] );

/**
 * Allocate a blank libvlc instance, also setting the exit handler.
 * Vlc's threading system must have been initialized first
 */
libvlc_int_t * libvlc_InternalCreate( void )
{
    libvlc_int_t *p_libvlc;
    libvlc_priv_t *priv;

    /* Allocate a libvlc instance object */
    p_libvlc = vlc_custom_create( (vlc_object_t *)NULL, sizeof (*priv),
                                  "libvlc" );
    if( p_libvlc == NULL )
        return NULL;

    priv = libvlc_priv (p_libvlc);
    priv->playlist = NULL;
    priv->p_vlm = NULL;

    vlc_ExitInit( &priv->exit );

    return p_libvlc;
}

/**
 * Initialize a libvlc instance
 * This function initializes a previously allocated libvlc instance:
 *  - CPU detection
 *  - gettext initialization
 *  - message queue, module bank and playlist initialization
 *  - configuration and commandline parsing
 */
int libvlc_InternalInit( libvlc_int_t *p_libvlc, int i_argc,
                         const char *ppsz_argv[] )
{
    libvlc_priv_t *priv = libvlc_priv (p_libvlc);
    char *       psz_modules = NULL;
    char *       psz_parser = NULL;
    char *       psz_control = NULL;
    char        *psz_val;

    /* System specific initialization code */
    system_Init();

    vlc_LogPreinit(p_libvlc);

    /* Initialize the module bank and load the configuration of the
     * core module. We need to do this at this stage to be able to display
     * a short help if required by the user. (short help == core module
     * options) */
    module_InitBank ();

    /* Get command line options that affect module loading. */
    if( config_LoadCmdLine( p_libvlc, i_argc, ppsz_argv, NULL ) )
    {
        module_EndBank (false);
        return VLC_EGENERIC;
    }

    vlc_threads_setup (p_libvlc);

    /* Load the builtins and plugins into the module_bank.
     * We have to do it before config_Load*() because this also gets the
     * list of configuration options exported by each module and loads their
     * default values. */
    size_t module_count = module_LoadPlugins (p_libvlc);

    /*
     * Override default configuration with config file settings
     */
    if( !var_InheritBool( p_libvlc, "ignore-config" ) )
    {
        if( var_InheritBool( p_libvlc, "reset-config" ) )
            config_SaveConfigFile( p_libvlc ); /* Save default config */
        else
            config_LoadConfigFile( p_libvlc );
    }

    /*
     * Override configuration with command line settings
     */
    int vlc_optind;
    if( config_LoadCmdLine( p_libvlc, i_argc, ppsz_argv, &vlc_optind ) )
    {
        vlc_LogDeinit (p_libvlc);
        module_EndBank (true);
        return VLC_EGENERIC;
    }

    vlc_LogInit(p_libvlc);

    /*
     * Support for gettext
     */
#if defined( ENABLE_NLS ) \
     && ( defined( HAVE_GETTEXT ) || defined( HAVE_INCLUDED_GETTEXT ) )
    vlc_bindtextdomain (PACKAGE_NAME);
#endif
    /*xgettext: Translate "C" to the language code: "fr", "en_GB", "nl", "ru"... */
    msg_Dbg( p_libvlc, "translation test: code is \"%s\"", _("C") );

    if (config_PrintHelp (VLC_OBJECT(p_libvlc)))
    {
        module_EndBank (true);
        exit(0);
    }

    if( module_count <= 1 )
    {
        msg_Err( p_libvlc, "No plugins found! Check your VLC installation.");
        vlc_LogDeinit (p_libvlc);
        module_EndBank (true);
        return VLC_ENOMOD;
    }

#ifdef HAVE_DAEMON
    /* Check for daemon mode */
    if( var_InheritBool( p_libvlc, "daemon" ) )
    {
        if( daemon( 1, 0) != 0 )
        {
            msg_Err( p_libvlc, "Unable to fork vlc to daemon mode" );
            vlc_LogDeinit (p_libvlc);
            module_EndBank (true);
            return VLC_ENOMEM;
        }

        /* lets check if we need to write the pidfile */
        char *pidfile = var_InheritString( p_libvlc, "pidfile" );
        if( pidfile != NULL )
        {
            FILE *stream = vlc_fopen( pidfile, "w" );
            if( stream != NULL )
            {
                fprintf( stream, "%d", (int)getpid() );
                fclose( stream );
                msg_Dbg( p_libvlc, "written PID file %s", pidfile );
            }
            else
                msg_Err( p_libvlc, "cannot write PID file %s: %s",
                         pidfile, vlc_strerror_c(errno) );
            free( pidfile );
        }
    }
    else
    {
        var_Create( p_libvlc, "pidfile", VLC_VAR_STRING );
        var_SetString( p_libvlc, "pidfile", "" );
    }
#endif

    if( libvlc_InternalDialogInit( p_libvlc ) != VLC_SUCCESS )
    {
        vlc_LogDeinit (p_libvlc);
        module_EndBank (true);
        return VLC_ENOMEM;
    }
    if( libvlc_InternalKeystoreInit( p_libvlc ) != VLC_SUCCESS )
        msg_Warn( p_libvlc, "memory keystore init failed" );

/* FIXME: could be replaced by using Unix sockets */
#ifdef HAVE_DBUS

#define MPRIS_APPEND "/org/mpris/MediaPlayer2/TrackList/Append"
#define MPRIS_BUS_NAME "org.mpris.MediaPlayer2.vlc"
#define MPRIS_OBJECT_PATH "/org/mpris/MediaPlayer2"
#define MPRIS_TRACKLIST_INTERFACE "org.mpris.MediaPlayer2.TrackList"

    if( var_InheritBool( p_libvlc, "one-instance" )
    || ( var_InheritBool( p_libvlc, "one-instance-when-started-from-file" )
      && var_InheritBool( p_libvlc, "started-from-file" ) ) )
    {
        for( int i = vlc_optind; i < i_argc; i++ )
            if( ppsz_argv[i][0] == ':' )
            {
                msg_Err( p_libvlc, "item option %s incompatible with single instance",
                         ppsz_argv[i] );
                goto dbus_out;
            }

        /* Initialise D-Bus interface, check for other instances */
        dbus_threads_init_default();

        DBusError err;
        dbus_error_init( &err );

        /* connect to the session bus */
        DBusConnection  *conn = dbus_bus_get( DBUS_BUS_SESSION, &err );
        if( conn == NULL )
        {
            msg_Err( p_libvlc, "Failed to connect to D-Bus session daemon: %s",
                    err.message );
            dbus_error_free( &err );
            goto dbus_out;
        }

        /* check if VLC is available on the bus
         * if not: D-Bus control is not enabled on the other
         * instance and we can't pass MRLs to it */
        /* FIXME: This check is totally brain-dead and buggy. */
        if( !dbus_bus_name_has_owner( conn, MPRIS_BUS_NAME, &err ) )
        {
            dbus_connection_unref( conn );
            if( dbus_error_is_set( &err ) )
            {
                msg_Err( p_libvlc, "D-Bus error: %s", err.message );
            }
            else
                msg_Dbg( p_libvlc, "No media player running. Continuing normally." );
            dbus_error_free( &err );
            goto dbus_out;
        }

        const dbus_bool_t play = !var_InheritBool( p_libvlc, "playlist-enqueue" );

        msg_Warn( p_libvlc, "media player running. Exiting...");
        for( int i = vlc_optind; i < i_argc; i++ )
        {
            DBusMessage *msg = dbus_message_new_method_call(
               MPRIS_BUS_NAME, MPRIS_OBJECT_PATH, MPRIS_TRACKLIST_INTERFACE, "AddTrack" );
            if( unlikely(msg == NULL) )
                continue;

            /* We need to resolve relative paths in this instance */
            char *mrl;
            if( strstr( ppsz_argv[i], "://" ) )
                mrl = strdup( ppsz_argv[i] );
            else
                mrl = vlc_path2uri( ppsz_argv[i], NULL );
            if( mrl == NULL )
            {
                dbus_message_unref( msg );
                continue;
            }

            const char *after_track = MPRIS_APPEND;

            /* append MRLs */
            if( !dbus_message_append_args( msg, DBUS_TYPE_STRING, &mrl,
                                                DBUS_TYPE_OBJECT_PATH, &after_track,
                                                DBUS_TYPE_BOOLEAN, &play,
                                                DBUS_TYPE_INVALID ) )
            {
                 dbus_message_unref( msg );
                 msg = NULL;
                 free( mrl );
                 continue;
            }

            msg_Dbg( p_libvlc, "Adds %s to the running media player", mrl );
            free( mrl );

            /* send message and get a handle for a reply */
            DBusMessage *reply = dbus_connection_send_with_reply_and_block( conn, msg, -1,
                                                                            &err );
            dbus_message_unref( msg );
            if( reply == NULL )
            {
                msg_Err( p_libvlc, "D-Bus error: %s", err.message );
                continue;
            }
            dbus_message_unref( reply );
        }
        /* we unreference the connection when we've finished with it */
        dbus_connection_unref( conn );
        exit( 0 );
    }
#undef MPRIS_APPEND
#undef MPRIS_BUS_NAME
#undef MPRIS_OBJECT_PATH
#undef MPRIS_TRACKLIST_INTERFACE
dbus_out:
#endif // HAVE_DBUS

    vlc_CPU_dump( VLC_OBJECT(p_libvlc) );

    priv->b_stats = var_InheritBool( p_libvlc, "stats" );

    /*
     * Initialize hotkey handling
     */
    priv->actions = vlc_InitActions( p_libvlc );

    /*
     * Meta data handling
     */
    priv->parser = playlist_preparser_New(VLC_OBJECT(p_libvlc));

    /* Create a variable for showing the fullscreen interface */
    var_Create( p_libvlc, "intf-toggle-fscontrol", VLC_VAR_BOOL );
    var_SetBool( p_libvlc, "intf-toggle-fscontrol", true );

    /* Create a variable for the Boss Key */
    var_Create( p_libvlc, "intf-boss", VLC_VAR_VOID );

    /* Create a variable for showing the main interface */
    var_Create( p_libvlc, "intf-show", VLC_VAR_BOOL );

    /* Create a variable for showing the right click menu */
    var_Create( p_libvlc, "intf-popupmenu", VLC_VAR_BOOL );

    /* variables for signalling creation of new files */
    var_Create( p_libvlc, "snapshot-file", VLC_VAR_STRING );
    var_Create( p_libvlc, "record-file", VLC_VAR_STRING );

    /* some default internal settings */
    var_Create( p_libvlc, "window", VLC_VAR_STRING );
    /* NOTE: Because the playlist and interfaces start before this function
     * returns control to the application (DESIGN BUG!), all these variables
     * must be created (in place of libvlc_new()) and set to VLC defaults
     * (in place of VLC main()) *here*. */
    var_Create( p_libvlc, "user-agent", VLC_VAR_STRING );
    var_SetString( p_libvlc, "user-agent",
                   "VLC media player (LibVLC "VERSION")" );
    var_Create( p_libvlc, "http-user-agent", VLC_VAR_STRING );
    var_SetString( p_libvlc, "http-user-agent",
                   "VLC/"PACKAGE_VERSION" LibVLC/"PACKAGE_VERSION );
    var_Create( p_libvlc, "app-icon-name", VLC_VAR_STRING );
    var_SetString( p_libvlc, "app-icon-name", PACKAGE_NAME );
    var_Create( p_libvlc, "app-id", VLC_VAR_STRING );
    var_SetString( p_libvlc, "app-id", "org.VideoLAN.VLC" );
    var_Create( p_libvlc, "app-version", VLC_VAR_STRING );
    var_SetString( p_libvlc, "app-version", PACKAGE_VERSION );

    /* System specific configuration */
    system_Configure( p_libvlc, i_argc - vlc_optind, ppsz_argv + vlc_optind );

#ifdef ENABLE_VLM
    /* Initialize VLM if vlm-conf is specified */
    psz_parser = var_CreateGetNonEmptyString( p_libvlc, "vlm-conf" );
    if( psz_parser )
    {
        priv->p_vlm = vlm_New( p_libvlc );
        if( !priv->p_vlm )
            msg_Err( p_libvlc, "VLM initialization failed" );
    }
    free( psz_parser );
#endif

    /*
     * Load background interfaces
     */
    psz_modules = var_CreateGetNonEmptyString( p_libvlc, "extraintf" );
    psz_control = var_CreateGetNonEmptyString( p_libvlc, "control" );

    if( psz_modules && psz_control )
    {
        char* psz_tmp;
        if( asprintf( &psz_tmp, "%s:%s", psz_modules, psz_control ) != -1 )
        {
            free( psz_modules );
            psz_modules = psz_tmp;
        }
    }
    else if( psz_control )
    {
        free( psz_modules );
        psz_modules = strdup( psz_control );
    }

    psz_parser = psz_modules;
    while ( psz_parser && *psz_parser )
    {
        char *psz_module, *psz_temp;
        psz_module = psz_parser;
        psz_parser = strchr( psz_module, ':' );
        if ( psz_parser )
        {
            *psz_parser = '\0';
            psz_parser++;
        }
        if( asprintf( &psz_temp, "%s,none", psz_module ) != -1)
        {
            libvlc_InternalAddIntf( p_libvlc, psz_temp );
            free( psz_temp );
        }
    }
    free( psz_modules );
    free( psz_control );

    if( var_InheritBool( p_libvlc, "network-synchronisation") )
        libvlc_InternalAddIntf( p_libvlc, "netsync,none" );

#ifdef __APPLE__
    var_Create( p_libvlc, "drawable-view-top", VLC_VAR_INTEGER );
    var_Create( p_libvlc, "drawable-view-left", VLC_VAR_INTEGER );
    var_Create( p_libvlc, "drawable-view-bottom", VLC_VAR_INTEGER );
    var_Create( p_libvlc, "drawable-view-right", VLC_VAR_INTEGER );
    var_Create( p_libvlc, "drawable-clip-top", VLC_VAR_INTEGER );
    var_Create( p_libvlc, "drawable-clip-left", VLC_VAR_INTEGER );
    var_Create( p_libvlc, "drawable-clip-bottom", VLC_VAR_INTEGER );
    var_Create( p_libvlc, "drawable-clip-right", VLC_VAR_INTEGER );
    var_Create( p_libvlc, "drawable-nsobject", VLC_VAR_ADDRESS );
#endif

    /*
     * Get input filenames given as commandline arguments.
     * We assume that the remaining parameters are filenames
     * and their input options.
     */
    GetFilenames( p_libvlc, i_argc - vlc_optind, ppsz_argv + vlc_optind );

    /*
     * Get --open argument
     */
    psz_val = var_InheritString( p_libvlc, "open" );
    if ( psz_val != NULL )
    {
        intf_InsertItem( p_libvlc, psz_val, 0, NULL, 0 );
        free( psz_val );
    }

    return VLC_SUCCESS;
}

/**
 * Cleanup a libvlc instance. The instance is not completely deallocated
 * \param p_libvlc the instance to clean
 */
void libvlc_InternalCleanup( libvlc_int_t *p_libvlc )
{
    libvlc_priv_t *priv = libvlc_priv (p_libvlc);

    /* Ask the interfaces to stop and destroy them */
    msg_Dbg( p_libvlc, "removing all interfaces" );
    libvlc_Quit( p_libvlc );
    intf_DestroyAll( p_libvlc );

    libvlc_InternalDialogClean( p_libvlc );
    libvlc_InternalKeystoreClean( p_libvlc );

#ifdef ENABLE_VLM
    /* Destroy VLM if created in libvlc_InternalInit */
    if( priv->p_vlm )
    {
        vlm_Delete( priv->p_vlm );
    }
#endif

#if !defined( _WIN32 ) && !defined( __OS2__ )
    char *pidfile = var_InheritString( p_libvlc, "pidfile" );
    if( pidfile != NULL )
    {
        msg_Dbg( p_libvlc, "removing PID file %s", pidfile );
        if( unlink( pidfile ) )
            msg_Warn( p_libvlc, "cannot remove PID file %s: %s",
                      pidfile, vlc_strerror_c(errno) );
        free( pidfile );
    }
#endif

    if (priv->parser != NULL)
        playlist_preparser_Delete(priv->parser);

    vlc_DeinitActions( p_libvlc, priv->actions );

    /* Save the configuration */
    if( !var_InheritBool( p_libvlc, "ignore-config" ) )
        config_AutoSaveConfigFile( VLC_OBJECT(p_libvlc) );

    /* Free module bank. It is refcounted, so we call this each time  */
    vlc_LogDeinit (p_libvlc);
    module_EndBank (true);
#if defined(_WIN32) || defined(__OS2__)
    system_End( );
#endif
}

/**
 * Destroy everything.
 * This function requests the running threads to finish, waits for their
 * termination, and destroys their structure.
 * It stops the thread systems: no instance can run after this has run
 * \param p_libvlc the instance to destroy
 */
void libvlc_InternalDestroy( libvlc_int_t *p_libvlc )
{
    libvlc_priv_t *priv = libvlc_priv( p_libvlc );

    vlc_ExitDestroy( &priv->exit );

    assert( atomic_load(&(vlc_internals(p_libvlc)->refs)) == 1 );
    vlc_object_release( p_libvlc );
}

/*****************************************************************************
 * GetFilenames: parse command line options which are not flags
 *****************************************************************************
 * Parse command line for input files as well as their associated options.
 * An option always follows its associated input and begins with a ":".
 *****************************************************************************/
static void GetFilenames( libvlc_int_t *p_vlc, unsigned n,
                          const char *const args[] )
{
    while( n > 0 )
    {
        /* Count the input options */
        unsigned i_options = 0;

        while( args[--n][0] == ':' )
        {
            i_options++;
            if( n == 0 )
            {
                msg_Warn( p_vlc, "options %s without item", args[n] );
                return; /* syntax!? */
            }
        }

        char *mrl = NULL;
        if( strstr( args[n], "://" ) == NULL )
        {
            mrl = vlc_path2uri( args[n], NULL );
            if( !mrl )
                continue;
        }

        intf_InsertItem( p_vlc, (mrl != NULL) ? mrl : args[n], i_options,
                         ( i_options ? &args[n + 1] : NULL ),
                         VLC_INPUT_OPTION_TRUSTED );
        free( mrl );
    }
}

/**
 * Requests extraction of the meta data for an input item (a.k.a. preparsing).
 * The actual extraction is asynchronous.
 */
int libvlc_MetaRequest(libvlc_int_t *libvlc, input_item_t *item,
                       input_item_meta_request_option_t i_options)
{
    libvlc_priv_t *priv = libvlc_priv(libvlc);

    if (unlikely(priv->parser == NULL))
        return VLC_ENOMEM;

    vlc_mutex_lock( &item->lock );
    if( item->i_preparse_depth == 0 )
        item->i_preparse_depth = 1;
    if( i_options & META_REQUEST_OPTION_DO_INTERACT )
        item->b_preparse_interact = true;
    vlc_mutex_unlock( &item->lock );
    playlist_preparser_Push(priv->parser, item, i_options);
    return VLC_SUCCESS;
}

/**
 * Requests retrieving/downloading art for an input item.
 * The retrieval is performed asynchronously.
 */
int libvlc_ArtRequest(libvlc_int_t *libvlc, input_item_t *item,
                      input_item_meta_request_option_t i_options)
{
    libvlc_priv_t *priv = libvlc_priv(libvlc);

    if (unlikely(priv->parser == NULL))
        return VLC_ENOMEM;

    playlist_preparser_fetcher_Push(priv->parser, item, i_options);
    return VLC_SUCCESS;
}
