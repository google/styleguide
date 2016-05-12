/*****************************************************************************
 * libvlc.h: Internal libvlc generic/misc declaration
 *****************************************************************************
 * Copyright (C) 1999, 2000, 2001, 2002 VLC authors and VideoLAN
 * Copyright © 2006-2007 Rémi Denis-Courmont
 * $Id: 21bdfdcfba26f0a50e775a077df02a1debe88ba6 $
 *
 * Authors: Vincent Seguin <seguin@via.ecp.fr>
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

#ifndef LIBVLC_LIBVLC_H
# define LIBVLC_LIBVLC_H 1

extern const char psz_vlc_changeset[];

typedef struct variable_t variable_t;

/* Actions (hot keys) */
struct vlc_actions;
struct vlc_actions *vlc_InitActions (libvlc_int_t *);
extern void vlc_DeinitActions (libvlc_int_t *, struct vlc_actions *);

/*
 * OS-specific initialization
 */
void system_Init      ( void );
void system_Configure ( libvlc_int_t *, int, const char *const [] );
#if defined(_WIN32) || defined(__OS2__)
void system_End(void);
#ifndef __OS2__
size_t EnumClockSource( vlc_object_t *, const char *, char ***, char *** );
#endif
#endif
void vlc_CPU_init(void);
void vlc_CPU_dump(vlc_object_t *);

/*
 * Threads subsystem
 */

/* This cannot be used as is from plugins yet: */
int vlc_clone_detach (vlc_thread_t *, void *(*)(void *), void *, int);

int vlc_set_priority( vlc_thread_t, int );

void vlc_threads_setup (libvlc_int_t *);

void vlc_trace (const char *fn, const char *file, unsigned line);
#define vlc_backtrace() vlc_trace(__func__, __FILE__, __LINE__)

#if (defined (LIBVLC_USE_PTHREAD) || defined(__ANDROID__)) && !defined (NDEBUG)
void vlc_assert_locked (vlc_mutex_t *);
#else
# define vlc_assert_locked( m ) (void)m
#endif

/*
 * Logging
 */
typedef struct vlc_logger_t vlc_logger_t;

int vlc_LogPreinit(libvlc_int_t *);
int vlc_LogInit(libvlc_int_t *);
void vlc_LogDeinit(libvlc_int_t *);

/*
 * LibVLC exit event handling
 */
typedef struct vlc_exit
{
    vlc_mutex_t lock;
    void (*handler) (void *);
    void *opaque;
} vlc_exit_t;

void vlc_ExitInit( vlc_exit_t * );
void vlc_ExitDestroy( vlc_exit_t * );

/*
 * LibVLC objects stuff
 */

/**
 * Creates a VLC object.
 *
 * Note that because the object name pointer must remain valid, potentially
 * even after the destruction of the object (through the message queues), this
 * function CANNOT be exported to plugins as is. In this case, the old
 * vlc_object_create() must be used instead.
 *
 * @param p_this an existing VLC object
 * @param i_size byte size of the object structure
 * @param psz_type object type name
 * @return the created object, or NULL.
 */
extern void *
vlc_custom_create (vlc_object_t *p_this, size_t i_size, const char *psz_type);
#define vlc_custom_create(o, s, n) \
        vlc_custom_create(VLC_OBJECT(o), s, n)

/**
 * Assign a name to an object for vlc_object_find_name().
 */
extern int vlc_object_set_name(vlc_object_t *, const char *);
#define vlc_object_set_name(o, n) vlc_object_set_name(VLC_OBJECT(o), n)

/* Types */
typedef void (*vlc_destructor_t) (struct vlc_object_t *);
void vlc_object_set_destructor (vlc_object_t *, vlc_destructor_t);
#define vlc_object_set_destructor(a,b) \
        vlc_object_set_destructor (VLC_OBJECT(a), b)

#define ZOOM_SECTION N_("Zoom")
#define ZOOM_QUARTER_KEY_TEXT N_("1:4 Quarter")
#define ZOOM_HALF_KEY_TEXT N_("1:2 Half")
#define ZOOM_ORIGINAL_KEY_TEXT N_("1:1 Original")
#define ZOOM_DOUBLE_KEY_TEXT N_("2:1 Double")

/**
 * Private LibVLC instance data.
 */
typedef struct vlc_dialog_provider vlc_dialog_provider;
typedef struct vlc_keystore vlc_keystore;

typedef struct libvlc_priv_t
{
    libvlc_int_t       public_data;

    /* Logging */
    bool               b_stats;     ///< Whether to collect stats

    /* Singleton objects */
    vlc_logger_t      *logger;
    vlm_t             *p_vlm;  ///< the VLM singleton (or NULL)
    vlc_dialog_provider *p_dialog_provider; ///< dialog provider
    vlc_keystore      *p_memory_keystore; ///< memory keystore
    struct playlist_t *playlist; ///< Playlist for interfaces
    struct playlist_preparser_t *parser; ///< Input item meta data handler
    struct vlc_actions *actions; ///< Hotkeys handler

    /* Exit callback */
    vlc_exit_t       exit;
} libvlc_priv_t;

static inline libvlc_priv_t *libvlc_priv (libvlc_int_t *libvlc)
{
    return (libvlc_priv_t *)libvlc;
}

void intf_InsertItem(libvlc_int_t *, const char *mrl, unsigned optc,
                     const char * const *optv, unsigned flags);
void intf_DestroyAll( libvlc_int_t * );

#define libvlc_stats( o ) (libvlc_priv((VLC_OBJECT(o))->p_libvlc)->b_stats)

/*
 * Variables stuff
 */
void var_OptionParse (vlc_object_t *, const char *, bool trusted);

/*
 * Stats stuff
 */
enum
{
    STATS_COUNTER,
    STATS_DERIVATIVE,
};

typedef struct counter_sample_t
{
    uint64_t value;
    mtime_t  date;
} counter_sample_t;

typedef struct counter_t
{
    int                 i_compute_type;
    int                 i_samples;
    counter_sample_t ** pp_samples;

    mtime_t             last_update;
} counter_t;

enum
{
    STATS_INPUT_BITRATE,
    STATS_READ_BYTES,
    STATS_READ_PACKETS,
    STATS_DEMUX_READ,
    STATS_DEMUX_BITRATE,
    STATS_DEMUX_CORRUPTED,
    STATS_DEMUX_DISCONTINUITY,
    STATS_PLAYED_ABUFFERS,
    STATS_LOST_ABUFFERS,
    STATS_DECODED_AUDIO,
    STATS_DECODED_VIDEO,
    STATS_DECODED_SUB,
    STATS_CLIENT_CONNECTIONS,
    STATS_ACTIVE_CONNECTIONS,
    STATS_SOUT_SENT_PACKETS,
    STATS_SOUT_SENT_BYTES,
    STATS_SOUT_SEND_BITRATE,
    STATS_DISPLAYED_PICTURES,
    STATS_LOST_PICTURES,
};

counter_t * stats_CounterCreate (int);
void stats_Update (counter_t *, uint64_t, uint64_t *);
void stats_CounterClean (counter_t * );

void stats_ComputeInputStats(input_thread_t*, input_stats_t*);
void stats_ReinitInputStats(input_stats_t *);

#endif
