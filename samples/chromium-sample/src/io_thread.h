// Copyright (c) 2012 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#ifndef CHROME_BROWSER_IO_THREAD_H_
#define CHROME_BROWSER_IO_THREAD_H_

#include <stddef.h>
#include <stdint.h>

#include <map>
#include <memory>
#include <set>
#include <string>
#include <unordered_set>
#include <vector>

#include "base/compiler_specific.h"
#include "base/macros.h"
#include "base/memory/ref_counted.h"
#include "base/memory/weak_ptr.h"
#include "base/strings/string_piece.h"
#include "base/time/time.h"
#include "build/build_config.h"
#include "chrome/browser/net/chrome_network_delegate.h"
#include "chrome/common/features.h"
#include "components/prefs/pref_member.h"
#include "components/ssl_config/ssl_config_service_manager.h"
#include "content/public/browser/browser_thread.h"
#include "content/public/browser/browser_thread_delegate.h"
#include "net/base/network_change_notifier.h"
#include "net/http/http_network_session.h"

class PrefProxyConfigTracker;
class PrefService;
class PrefRegistrySimple;
class SystemURLRequestContextGetter;

namespace base {
class CommandLine;
}

#if BUILDFLAG(ANDROID_JAVA_UI)
namespace chrome {
namespace android {
class ExternalDataUseObserver;
}
}
#endif  // BUILDFLAG(ANDROID_JAVA_UI)

namespace chrome_browser_net {
class DnsProbeService;
}

namespace data_usage {
class DataUseAggregator;
}

namespace extensions {
class EventRouterForwarder;
}

namespace net {
class CTPolicyEnforcer;
class CertVerifier;
class ChannelIDService;
class CookieStore;
class CTLogVerifier;
class FtpTransactionFactory;
class HostMappingRules;
class HostResolver;
class HttpAuthHandlerRegistryFactory;
class HttpAuthPreferences;
class HttpServerProperties;
class HttpTransactionFactory;
class HttpUserAgentSettings;
class NetworkDelegate;
class NetworkQualityEstimator;
class ProxyConfigService;
class ProxyService;
class SSLConfigService;
class TransportSecurityState;
class URLRequestBackoffManager;
class URLRequestContext;
class URLRequestContextGetter;
class URLRequestJobFactory;
}  // namespace net

namespace net_log {
class ChromeNetLog;
}

namespace policy {
class PolicyService;
}  // namespace policy

namespace test {
class IOThreadPeer;
}  // namespace test

// Contains state associated with, initialized and cleaned up on, and
// primarily used on, the IO thread.
//
// If you are looking to interact with the IO thread (e.g. post tasks
// to it or check if it is the current thread), see
// content::BrowserThread.
class IOThread : public content::BrowserThreadDelegate {
 public:
  struct Globals {
    class SystemRequestContextLeakChecker {
     public:
      explicit SystemRequestContextLeakChecker(Globals* globals);
      ~SystemRequestContextLeakChecker();

     private:
      Globals* const globals_;
    };

    Globals();
    ~Globals();

    // Global aggregator of data use. It must outlive the
    // |system_network_delegate|.
    std::unique_ptr<data_usage::DataUseAggregator> data_use_aggregator;
#if BUILDFLAG(ANDROID_JAVA_UI)
    // An external observer of data use.
    std::unique_ptr<chrome::android::ExternalDataUseObserver>
        external_data_use_observer;
#endif  // BUILDFLAG(ANDROID_JAVA_UI)
    // The "system" NetworkDelegate, used for Profile-agnostic network events.
    std::unique_ptr<net::NetworkDelegate> system_network_delegate;
    std::unique_ptr<net::HostResolver> host_resolver;
    std::unique_ptr<net::CertVerifier> cert_verifier;
    // The ChannelIDService must outlive the HttpTransactionFactory.
    std::unique_ptr<net::ChannelIDService> system_channel_id_service;
    // This TransportSecurityState doesn't load or save any state. It's only
    // used to enforce pinning for system requests and will only use built-in
    // pins.
    std::unique_ptr<net::TransportSecurityState> transport_security_state;
    std::vector<scoped_refptr<const net::CTLogVerifier>> ct_logs;
    std::unique_ptr<net::CTVerifier> cert_transparency_verifier;
    std::unique_ptr<net::CTPolicyEnforcer> ct_policy_enforcer;
    scoped_refptr<net::SSLConfigService> ssl_config_service;
    std::unique_ptr<net::HttpAuthHandlerFactory> http_auth_handler_factory;
    std::unique_ptr<net::HttpServerProperties> http_server_properties;
    std::unique_ptr<net::ProxyService> proxy_script_fetcher_proxy_service;
    std::unique_ptr<net::HttpNetworkSession>
        proxy_script_fetcher_http_network_session;
    std::unique_ptr<net::HttpTransactionFactory>
        proxy_script_fetcher_http_transaction_factory;
    std::unique_ptr<net::FtpTransactionFactory>
        proxy_script_fetcher_ftp_transaction_factory;
    std::unique_ptr<net::URLRequestJobFactory>
        proxy_script_fetcher_url_request_job_factory;
    std::unique_ptr<net::URLRequestBackoffManager> url_request_backoff_manager;
    std::unique_ptr<net::HttpAuthPreferences> http_auth_preferences;
    // TODO(willchan): Remove proxy script fetcher context since it's not
    // necessary now that I got rid of refcounting URLRequestContexts.
    //
    // The first URLRequestContext is |system_url_request_context|. We introduce
    // |proxy_script_fetcher_context| for the second context. It has a direct
    // ProxyService, since we always directly connect to fetch the PAC script.
    std::unique_ptr<net::URLRequestContext> proxy_script_fetcher_context;
    std::unique_ptr<net::ProxyService> system_proxy_service;
    std::unique_ptr<net::HttpNetworkSession> system_http_network_session;
    std::unique_ptr<net::HttpTransactionFactory>
        system_http_transaction_factory;
    std::unique_ptr<net::URLRequestJobFactory> system_url_request_job_factory;
    std::unique_ptr<net::URLRequestContext> system_request_context;
    SystemRequestContextLeakChecker system_request_context_leak_checker;
    // |system_cookie_store| and |system_channel_id_service| are shared
    // between |proxy_script_fetcher_context| and |system_request_context|.
    std::unique_ptr<net::CookieStore> system_cookie_store;
#if defined(ENABLE_EXTENSIONS)
    scoped_refptr<extensions::EventRouterForwarder>
        extension_event_router_forwarder;
#endif
    std::unique_ptr<net::HostMappingRules> host_mapping_rules;
    std::unique_ptr<net::HttpUserAgentSettings> http_user_agent_settings;
    std::unique_ptr<net::NetworkQualityEstimator> network_quality_estimator;

    // NetErrorTabHelper uses |dns_probe_service| to send DNS probes when a
    // main frame load fails with a DNS error in order to provide more useful
    // information to the renderer so it can show a more specific error page.
    std::unique_ptr<chrome_browser_net::DnsProbeService> dns_probe_service;

    // Enables Brotli Content-Encoding support
    bool enable_brotli;
  };

  // Helper class to configure HttpNetworkSession::Params and
  // HttpServerProperties based on field trials, policy, and command line.
  class NetworkSessionConfigurator {
   public:
    // Configure |params| based on field trials and policy arguments.
    static void ParseFieldTrials(bool is_spdy_allowed_by_policy,
                                 bool is_quic_allowed_by_policy,
                                 net::HttpNetworkSession::Params* params);

    // Configure |params| based on field trials, policy arguments,
    // and command line.
    static void ParseFieldTrialsAndCommandLine(
        bool is_spdy_allowed_by_policy,
        bool is_quic_allowed_by_policy,
        net::HttpNetworkSession::Params* params);

   private:
    // Map from name to value for all parameters associate with a field trial.
    using VariationParameters = std::map<std::string, std::string>;

    static void ParseFieldTrialsAndCommandLineInternal(
        const base::CommandLine& command_line,
        bool is_spdy_allowed_by_policy,
        bool is_quic_allowed_by_policy,
        net::HttpNetworkSession::Params* params);

    // Configures Alternative Services based on command line options and the
    // field trial group.
    static void ConfigureAltSvcParams(const base::CommandLine& command_line,
                                      base::StringPiece altsvc_trial_group,
                                      net::HttpNetworkSession::Params* params);

    // Configures QUIC options based on the flags in |command_line| as well as
    // the QUIC field trial group and parameters.  Must be called before
    // ConfigureSpdyParams.
    static void ConfigureQuicParams(
        const base::CommandLine& command_line,
        base::StringPiece quic_trial_group,
        const VariationParameters& quic_trial_params,
        bool is_quic_allowed_by_policy,
        net::HttpNetworkSession::Params* params);

    // Configures available SPDY protocol versions and parameters based on
    // command line flags as well as SPDY field trial group and parameters.
    // Must be called after ConfigureQuicParams.
    static void ConfigureSpdyParams(
        const base::CommandLine& command_line,
        base::StringPiece spdy_trial_group,
        const VariationParameters& spdy_trial_params,
        bool is_spdy_allowed_by_policy,
        net::HttpNetworkSession::Params* params);

    // Configure TCP FastOpen based on the field trial group.
    static void ConfigureTCPFastOpenParams(
        base::StringPiece tfo_trial_group,
        net::HttpNetworkSession::Params* params);

    // Configures NPN based on command line and the field trial group.
    static void ConfigureNPNParams(const base::CommandLine& command_line,
                                   base::StringPiece npn_trial_group,
                                   net::HttpNetworkSession::Params* params);

    // Configures the use of priority dependencies based on the field trial
    // group.
    static void ConfigurePriorityDependencies(
        base::StringPiece priority_dependencies_trial_group,
        net::HttpNetworkSession::Params* params);

    // Returns true if QUIC should be disabled when a connection times out with
    // open streams.
    static bool ShouldDisableQuicWhenConnectionTimesOutWithOpenStreams(
        const VariationParameters& quic_trial_params);

    // Returns true if QUIC should be enabled, either as a result of a field
    // trial or a command line flag.
    static bool ShouldEnableQuic(const base::CommandLine& command_line,
                                 base::StringPiece quic_trial_group,
                                 bool quic_allowed_by_policy);

    // Returns true if the selection of the ephemeral port in bind() should be
    // performed by Chromium, and false if the OS should select the port.  The
    // OS option is used to prevent Windows from posting a security warning
    // dialog.
    static bool ShouldEnableQuicPortSelection(
        const base::CommandLine& command_line);

    // Returns true if QUIC should always require handshake confirmation during
    // the QUIC handshake.
    static bool ShouldQuicAlwaysRequireHandshakeConfirmation(
        const VariationParameters& quic_trial_params);

    // Returns true if QUIC should disable connection pooling.
    static bool ShouldQuicDisableConnectionPooling(
        const VariationParameters& quic_trial_params);

    // Returns the ratio of time to load QUIC sever information from disk cache
    // to 'smoothed RTT' based on field trial. Returns 0 if there is an error
    // parsing the field trial params, or if the default value should be used.
    static float GetQuicLoadServerInfoTimeoutSrttMultiplier(
        const VariationParameters& quic_trial_params);

    // Returns true if QUIC's connection racing should be enabled.
    static bool ShouldQuicEnableConnectionRacing(
        const VariationParameters& quic_trial_params);

    // Returns true if QUIC's should use non-blocking IO.
    static bool ShouldQuicEnableNonBlockingIO(
        const VariationParameters& quic_trial_params);

    // Returns true if QUIC shouldn't load QUIC server information from the disk
    // cache.
    static bool ShouldQuicDisableDiskCache(
        const VariationParameters& quic_trial_params);

    // Returns true if QUIC should prefer AES-GCN even without hardware support.
    static bool ShouldQuicPreferAes(
        const VariationParameters& quic_trial_params);

    // Returns true if QUIC should enable alternative services for different
    // host.
    static bool ShouldQuicEnableAlternativeServicesForDifferentHost(
        const base::CommandLine& command_line,
        const VariationParameters& quic_trial_params);

    // Returns the maximum number of QUIC connections with high packet loss in a
    // row after which QUIC should be disabled.  Returns 0 if the default value
    // should be used.
    static int GetQuicMaxNumberOfLossyConnections(
        const VariationParameters& quic_trial_params);

    // Returns the packet loss rate in fraction after which a QUIC connection is
    // closed and is considered as a lossy connection. Returns 0 if the default
    // value should be used.
    static float GetQuicPacketLossThreshold(
        const VariationParameters& quic_trial_params);

    // Returns the size of the QUIC receive buffer to use, or 0 if the default
    // should be used.
    static int GetQuicSocketReceiveBufferSize(
        const VariationParameters& quic_trial_params);

    // Returns true if QUIC should close sessions when any of the client's IP
    // addresses change.
    static bool ShouldQuicCloseSessionsOnIpChange(
        const VariationParameters& quic_trial_params);

    // Returns the idle connection timeout for QUIC connections.  Returns 0 if
    // there is an error parsing any of the options, or if the default value
    // should be used.
    static int GetQuicIdleConnectionTimeoutSeconds(
        const VariationParameters& quic_trial_params);

    // Returns true if PreConnect should be disabled if QUIC can do 0RTT.
    static bool ShouldQuicDisablePreConnectIfZeroRtt(
        const VariationParameters& quic_trial_params);

    // Returns the set of hosts to whitelist for QUIC.
    static std::unordered_set<std::string> GetQuicHostWhitelist(
        const base::CommandLine& command_line,
        const VariationParameters& quic_trial_params);

    // Returns true if QUIC should migrate sessions when primary network
    // changes.
    static bool ShouldQuicMigrateSessionsOnNetworkChange(
        const VariationParameters& quic_trial_params);

    // Returns true if QUIC should migrate sessions early.
    static bool ShouldQuicMigrateSessionsEarly(
        const VariationParameters& quic_trial_params);

    // Returns the maximum length for QUIC packets, based on any flags in
    // |command_line| or the field trial.  Returns 0 if there is an error
    // parsing any of the options, or if the default value should be used.
    static size_t GetQuicMaxPacketLength(
        const base::CommandLine& command_line,
        const VariationParameters& quic_trial_params);

    // Returns the QUIC versions specified by any flags in |command_line| or
    // |quic_trial_params|.
    static net::QuicVersion GetQuicVersion(
        const base::CommandLine& command_line,
        const VariationParameters& quic_trial_params);

    // Returns the QUIC version specified by |quic_version| or
    // QUIC_VERSION_UNSUPPORTED if |quic_version| is invalid.
    static net::QuicVersion ParseQuicVersion(const std::string& quic_version);

    // Returns the QUIC connection options specified by any flags in
    // |command_line| or |quic_trial_params|.
    static net::QuicTagVector GetQuicConnectionOptions(
        const base::CommandLine& command_line,
        const VariationParameters& quic_trial_params);
  };

  // |net_log| must either outlive the IOThread or be NULL.
  IOThread(PrefService* local_state,
           policy::PolicyService* policy_service,
           net_log::ChromeNetLog* net_log,
           extensions::EventRouterForwarder* extension_event_router_forwarder);

  ~IOThread() override;

  static void RegisterPrefs(PrefRegistrySimple* registry);

  // Can only be called on the IO thread.
  Globals* globals();

  // Allows overriding Globals in tests where IOThread::Init() and
  // IOThread::CleanUp() are not called.  This allows for injecting mocks into
  // IOThread global objects.
  void SetGlobalsForTesting(Globals* globals);

  net_log::ChromeNetLog* net_log();

  // Handles changing to On The Record mode, discarding confidential data.
  void ChangedToOnTheRecord();

  // Returns a getter for the URLRequestContext.  Only called on the UI thread.
  net::URLRequestContextGetter* system_url_request_context_getter();

  // Clears the host cache.  Intended to be used to prevent exposing recently
  // visited sites on about:net-internals/#dns and about:dns pages.  Must be
  // called on the IO thread.
  void ClearHostCache();

  const net::HttpNetworkSession::Params& NetworkSessionParams() const;

  base::TimeTicks creation_time() const;

  // Returns the callback for updating data use prefs.
  const metrics::UpdateUsagePrefCallbackType& GetMetricsDataUseForwarder();

 private:
  // Provide SystemURLRequestContextGetter with access to
  // InitSystemRequestContext().
  friend class SystemURLRequestContextGetter;

  friend class test::IOThreadPeer;

  // BrowserThreadDelegate implementation, runs on the IO thread.
  // This handles initialization and destruction of state that must
  // live on the IO thread.
  void Init() override;
  void CleanUp() override;

  void InitializeNetworkOptions(const base::CommandLine& parsed_command_line);

  // Global state must be initialized on the IO thread, then this
  // method must be invoked on the UI thread.
  void InitSystemRequestContext();

  // Lazy initialization of system request context for
  // SystemURLRequestContextGetter. To be called on IO thread only
  // after global state has been initialized on the IO thread, and
  // SystemRequestContext state has been initialized on the UI thread.
  void InitSystemRequestContextOnIOThread();

  void CreateDefaultAuthHandlerFactory();

  // Returns an SSLConfigService instance.
  net::SSLConfigService* GetSSLConfigService();

  void ChangedToOnTheRecordOnIOThread();

  void UpdateDnsClientEnabled();
  void UpdateServerWhitelist();
  void UpdateDelegateWhitelist();
  void UpdateAndroidAuthNegotiateAccountType();
  void UpdateNegotiateDisableCnameLookup();
  void UpdateNegotiateEnablePort();

  extensions::EventRouterForwarder* extension_event_router_forwarder() {
#if defined(ENABLE_EXTENSIONS)
    return extension_event_router_forwarder_;
#else
    return NULL;
#endif
  }
  static net::URLRequestContext* ConstructSystemRequestContext(
      IOThread::Globals* globals,
      const net::HttpNetworkSession::Params& params,
      net::NetLog* net_log);

  // TODO(willchan): Remove proxy script fetcher context since it's not
  // necessary now that I got rid of refcounting URLRequestContexts.
  // See IOThread::Globals for details.
  static net::URLRequestContext* ConstructProxyScriptFetcherContext(
      IOThread::Globals* globals,
      const net::HttpNetworkSession::Params& params,
      net::NetLog* net_log);

  // The NetLog is owned by the browser process, to allow logging from other
  // threads during shutdown, but is used most frequently on the IOThread.
  net_log::ChromeNetLog* net_log_;

#if defined(ENABLE_EXTENSIONS)
  // The extensions::EventRouterForwarder allows for sending events to
  // extensions from the IOThread.
  extensions::EventRouterForwarder* extension_event_router_forwarder_;
#endif

  // These member variables are basically global, but their lifetimes are tied
  // to the IOThread.  IOThread owns them all, despite not using scoped_ptr.
  // This is because the destructor of IOThread runs on the wrong thread.  All
  // member variables should be deleted in CleanUp().

  // These member variables are initialized in Init() and do not change for the
  // lifetime of the IO thread.

  Globals* globals_;

  net::HttpNetworkSession::Params params_;
  NetworkSessionConfigurator network_session_configurator_;

  // Observer that logs network changes to the ChromeNetLog.
  class LoggingNetworkChangeObserver;
  std::unique_ptr<LoggingNetworkChangeObserver> network_change_observer_;

  BooleanPrefMember system_enable_referrers_;

  BooleanPrefMember dns_client_enabled_;

  BooleanPrefMember quick_check_enabled_;

  // Store HTTP Auth-related policies in this thread.
  // TODO(aberent) Make the list of auth schemes a PrefMember, so that the
  // policy can change after startup (https://crbug/549273).
  std::string auth_schemes_;
  BooleanPrefMember negotiate_disable_cname_lookup_;
  BooleanPrefMember negotiate_enable_port_;
  StringPrefMember auth_server_whitelist_;
  StringPrefMember auth_delegate_whitelist_;

#if defined(OS_ANDROID)
  StringPrefMember auth_android_negotiate_account_type_;
#endif
#if defined(OS_POSIX) && !defined(OS_ANDROID)
  // No PrefMember for the GSSAPI library name, since changing it after startup
  // requires unloading the existing GSSAPI library, which could cause all sorts
  // of problems for, for example, active Negotiate transactions.
  std::string gssapi_library_name_;
#endif

  // This is an instance of the default SSLConfigServiceManager for the current
  // platform and it gets SSL preferences from local_state object.
  std::unique_ptr<ssl_config::SSLConfigServiceManager>
      ssl_config_service_manager_;

  // These member variables are initialized by a task posted to the IO thread,
  // which gets posted by calling certain member functions of IOThread.
  std::unique_ptr<net::ProxyConfigService> system_proxy_config_service_;

  std::unique_ptr<PrefProxyConfigTracker> pref_proxy_config_tracker_;

  scoped_refptr<net::URLRequestContextGetter>
      system_url_request_context_getter_;

  // True if SPDY is allowed by policy.
  bool is_spdy_allowed_by_policy_;

  // True if QUIC is allowed by policy.
  bool is_quic_allowed_by_policy_;

  const base::TimeTicks creation_time_;

  // Callback for updating data use prefs which needs to be initialized on UI
  // thread and passed to |ChromeNetworkDelegate|.
  metrics::UpdateUsagePrefCallbackType metrics_data_use_forwarder_;

  base::WeakPtrFactory<IOThread> weak_factory_;

  DISALLOW_COPY_AND_ASSIGN(IOThread);
};

#endif  // CHROME_BROWSER_IO_THREAD_H_
