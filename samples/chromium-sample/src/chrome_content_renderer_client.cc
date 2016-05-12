// Copyright (c) 2012 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#include "chrome/renderer/chrome_content_renderer_client.h"

#include <memory>
#include <utility>

#include "base/command_line.h"
#include "base/debug/crash_logging.h"
#include "base/logging.h"
#include "base/macros.h"
#include "base/metrics/field_trial.h"
#include "base/metrics/histogram.h"
#include "base/metrics/user_metrics_action.h"
#include "base/strings/string_number_conversions.h"
#include "base/strings/string_util.h"
#include "base/strings/utf_string_conversions.h"
#include "base/time/time.h"
#include "base/values.h"
#include "build/build_config.h"
#include "chrome/common/channel_info.h"
#include "chrome/common/chrome_isolated_world_ids.h"
#include "chrome/common/chrome_paths.h"
#include "chrome/common/chrome_switches.h"
#include "chrome/common/crash_keys.h"
#include "chrome/common/pepper_permission_util.h"
#include "chrome/common/render_messages.h"
#include "chrome/common/secure_origin_whitelist.h"
#include "chrome/common/url_constants.h"
#include "chrome/grit/generated_resources.h"
#include "chrome/grit/locale_settings.h"
#include "chrome/grit/renderer_resources.h"
#include "chrome/renderer/banners/app_banner_client.h"
#include "chrome/renderer/benchmarking_extension.h"
#include "chrome/renderer/chrome_render_frame_observer.h"
#include "chrome/renderer/chrome_render_thread_observer.h"
#include "chrome/renderer/chrome_render_view_observer.h"
#include "chrome/renderer/content_settings_observer.h"
#include "chrome/renderer/external_extension.h"
#include "chrome/renderer/loadtimes_extension_bindings.h"
#include "chrome/renderer/media/chrome_key_systems.h"
#include "chrome/renderer/net/net_error_helper.h"
#include "chrome/renderer/net_benchmarking_extension.h"
#include "chrome/renderer/page_load_histograms.h"
#include "chrome/renderer/pepper/pepper_helper.h"
#include "chrome/renderer/plugins/non_loadable_plugin_placeholder.h"
#include "chrome/renderer/plugins/plugin_preroller.h"
#include "chrome/renderer/plugins/plugin_uma.h"
#include "chrome/renderer/prerender/prerender_dispatcher.h"
#include "chrome/renderer/prerender/prerender_helper.h"
#include "chrome/renderer/prerender/prerenderer_client.h"
#include "chrome/renderer/safe_browsing/phishing_classifier_delegate.h"
#include "chrome/renderer/safe_browsing/threat_dom_details.h"
#include "chrome/renderer/searchbox/search_bouncer.h"
#include "chrome/renderer/searchbox/searchbox.h"
#include "chrome/renderer/searchbox/searchbox_extension.h"
#include "chrome/renderer/tts_dispatcher.h"
#include "chrome/renderer/worker_content_settings_client_proxy.h"
#include "components/autofill/content/renderer/autofill_agent.h"
#include "components/autofill/content/renderer/password_autofill_agent.h"
#include "components/autofill/content/renderer/password_generation_agent.h"
#include "components/content_settings/core/common/content_settings_pattern.h"
#include "components/contextual_search/renderer/overlay_js_render_frame_observer.h"
#include "components/data_reduction_proxy/core/common/data_reduction_proxy_headers.h"
#include "components/dom_distiller/content/renderer/distillability_agent.h"
#include "components/dom_distiller/content/renderer/distiller_js_render_frame_observer.h"
#include "components/dom_distiller/core/url_constants.h"
#include "components/error_page/common/localized_error.h"
#include "components/network_hints/renderer/prescient_networking_dispatcher.h"
#include "components/page_load_metrics/renderer/metrics_render_frame_observer.h"
#include "components/password_manager/content/renderer/credential_manager_client.h"
#include "components/pdf/renderer/pepper_pdf_host.h"
#include "components/plugins/renderer/mobile_youtube_plugin.h"
#include "components/signin/core/common/profile_management_switches.h"
#include "components/startup_metric_utils/common/startup_metric_messages.h"
#include "components/version_info/version_info.h"
#include "components/visitedlink/renderer/visitedlink_slave.h"
#include "components/web_cache/renderer/web_cache_impl.h"
#include "content/public/common/content_constants.h"
#include "content/public/common/content_switches.h"
#include "content/public/common/url_constants.h"
#include "content/public/renderer/plugin_instance_throttler.h"
#include "content/public/renderer/render_frame.h"
#include "content/public/renderer/render_thread.h"
#include "content/public/renderer/render_view.h"
#include "content/public/renderer/render_view_visitor.h"
#include "extensions/common/constants.h"
#include "ipc/ipc_sync_channel.h"
#include "net/base/net_errors.h"
#include "ppapi/c/private/ppb_pdf.h"
#include "ppapi/shared_impl/ppapi_switches.h"
#include "third_party/WebKit/public/platform/URLConversion.h"
#include "third_party/WebKit/public/platform/WebCachePolicy.h"
#include "third_party/WebKit/public/platform/WebSecurityOrigin.h"
#include "third_party/WebKit/public/platform/WebURL.h"
#include "third_party/WebKit/public/platform/WebURLError.h"
#include "third_party/WebKit/public/platform/WebURLRequest.h"
#include "third_party/WebKit/public/platform/WebURLResponse.h"
#include "third_party/WebKit/public/web/WebCache.h"
#include "third_party/WebKit/public/web/WebDataSource.h"
#include "third_party/WebKit/public/web/WebDocument.h"
#include "third_party/WebKit/public/web/WebElement.h"
#include "third_party/WebKit/public/web/WebLocalFrame.h"
#include "third_party/WebKit/public/web/WebPluginContainer.h"
#include "third_party/WebKit/public/web/WebPluginParams.h"
#include "third_party/WebKit/public/web/WebSecurityPolicy.h"
#include "ui/base/l10n/l10n_util.h"
#include "ui/base/layout.h"
#include "ui/base/resource/resource_bundle.h"
#include "ui/base/webui/jstemplate_builder.h"
#include "widevine_cdm_version.h"  // In SHARED_INTERMEDIATE_DIR.

#if !defined(DISABLE_NACL)
#include "components/nacl/common/nacl_constants.h"
#include "components/nacl/renderer/nacl_helper.h"
#endif

#if defined(ENABLE_EXTENSIONS)
#include "chrome/common/extensions/chrome_extensions_client.h"
#include "chrome/renderer/extensions/chrome_extensions_renderer_client.h"
#include "extensions/common/extension_urls.h"
#include "extensions/common/switches.h"
#include "extensions/renderer/dispatcher.h"
#include "extensions/renderer/renderer_extension_registry.h"
#endif

#if defined(ENABLE_IPC_FUZZER)
#include "chrome/common/external_ipc_dumper.h"
#endif

#if defined(ENABLE_PLUGINS)
#include "chrome/renderer/plugins/chrome_plugin_placeholder.h"
#include "chrome/renderer/plugins/power_saver_info.h"
#endif

#if defined(ENABLE_PRINTING)
#include "chrome/common/chrome_content_client.h"
#include "chrome/renderer/printing/chrome_print_web_view_helper_delegate.h"
#include "components/printing/renderer/print_web_view_helper.h"
#include "printing/print_settings.h"
#endif

#if defined(ENABLE_PRINT_PREVIEW)
#include "chrome/renderer/pepper/chrome_pdf_print_client.h"
#endif

#if defined(ENABLE_SPELLCHECK)
#include "chrome/renderer/spellchecker/spellcheck.h"
#include "chrome/renderer/spellchecker/spellcheck_provider.h"
#endif

#if defined(ENABLE_WEBRTC)
#include "chrome/renderer/media/webrtc_logging_message_filter.h"
#endif

using autofill::AutofillAgent;
using autofill::PasswordAutofillAgent;
using autofill::PasswordGenerationAgent;
using base::ASCIIToUTF16;
using base::UserMetricsAction;
using blink::WebCache;
using blink::WebCachePolicy;
using blink::WebConsoleMessage;
using blink::WebDataSource;
using blink::WebDocument;
using blink::WebFrame;
using blink::WebLocalFrame;
using blink::WebPlugin;
using blink::WebPluginParams;
using blink::WebSecurityOrigin;
using blink::WebSecurityPolicy;
using blink::WebString;
using blink::WebURL;
using blink::WebURLError;
using blink::WebURLRequest;
using blink::WebURLResponse;
using blink::WebVector;
using content::PluginInstanceThrottler;
using content::RenderFrame;
using content::RenderThread;
using content::WebPluginInfo;
using extensions::Extension;

namespace {

// Whitelist PPAPI for Android Runtime for Chromium. (See crbug.com/383937)
#if defined(ENABLE_PLUGINS)
const char* const kPredefinedAllowedCameraDeviceOrigins[] = {
  "6EAED1924DB611B6EEF2A664BD077BE7EAD33B8F",
  "4EB74897CB187C7633357C2FE832E0AD6A44883A"
};

const char* const kPredefinedAllowedCompositorOrigins[] = {
  "6EAED1924DB611B6EEF2A664BD077BE7EAD33B8F",
  "4EB74897CB187C7633357C2FE832E0AD6A44883A"
};
#endif

#if defined(ENABLE_PLUGINS)
void AppendParams(const std::vector<base::string16>& additional_names,
                  const std::vector<base::string16>& additional_values,
                  WebVector<WebString>* existing_names,
                  WebVector<WebString>* existing_values) {
  DCHECK(additional_names.size() == additional_values.size());
  DCHECK(existing_names->size() == existing_values->size());

  size_t existing_size = existing_names->size();
  size_t total_size = existing_size + additional_names.size();

  WebVector<WebString> names(total_size);
  WebVector<WebString> values(total_size);

  for (size_t i = 0; i < existing_size; ++i) {
    names[i] = (*existing_names)[i];
    values[i] = (*existing_values)[i];
  }

  for (size_t i = 0; i < additional_names.size(); ++i) {
    names[existing_size + i] = additional_names[i];
    values[existing_size + i] = additional_values[i];
  }

  existing_names->swap(names);
  existing_values->swap(values);
}

// For certain sandboxed Pepper plugins, use the JavaScript Content Settings.
bool ShouldUseJavaScriptSettingForPlugin(const WebPluginInfo& plugin) {
  if (plugin.type != WebPluginInfo::PLUGIN_TYPE_PEPPER_IN_PROCESS &&
      plugin.type != WebPluginInfo::PLUGIN_TYPE_PEPPER_OUT_OF_PROCESS) {
    return false;
  }

#if !defined(DISABLE_NACL)
  // Treat Native Client invocations like JavaScript.
  if (plugin.name == ASCIIToUTF16(nacl::kNaClPluginName))
    return true;
#endif

#if defined(WIDEVINE_CDM_AVAILABLE) && defined(ENABLE_PEPPER_CDMS)
  // Treat CDM invocations like JavaScript.
  if (plugin.name == ASCIIToUTF16(kWidevineCdmDisplayName)) {
    DCHECK(plugin.type == WebPluginInfo::PLUGIN_TYPE_PEPPER_OUT_OF_PROCESS);
    return true;
  }
#endif  // defined(WIDEVINE_CDM_AVAILABLE) && defined(ENABLE_PEPPER_CDMS)

  return false;
}
#endif  // defined(ENABLE_PLUGINS)

#if defined(ENABLE_SPELLCHECK)
class SpellCheckReplacer : public content::RenderViewVisitor {
 public:
  explicit SpellCheckReplacer(SpellCheck* spellcheck)
      : spellcheck_(spellcheck) {}
  bool Visit(content::RenderView* render_view) override;

 private:
  SpellCheck* spellcheck_;  // New shared spellcheck for all views. Weak Ptr.
  DISALLOW_COPY_AND_ASSIGN(SpellCheckReplacer);
};

bool SpellCheckReplacer::Visit(content::RenderView* render_view) {
  SpellCheckProvider* provider = SpellCheckProvider::Get(render_view);
  DCHECK(provider);
  provider->set_spellcheck(spellcheck_);
  return true;
}
#endif

#if defined(ENABLE_EXTENSIONS)
bool IsStandaloneExtensionProcess() {
  return base::CommandLine::ForCurrentProcess()->HasSwitch(
      extensions::switches::kExtensionProcess);
}
#endif

// Defers media player loading in background pages until they're visible.
// TODO(dalecurtis): Include an idle listener too.  http://crbug.com/509135
class MediaLoadDeferrer : public content::RenderFrameObserver {
 public:
  MediaLoadDeferrer(content::RenderFrame* render_frame,
                    const base::Closure& continue_loading_cb)
      : content::RenderFrameObserver(render_frame),
        continue_loading_cb_(continue_loading_cb) {}
  ~MediaLoadDeferrer() override {}

 private:
  // content::RenderFrameObserver implementation:
  void WasShown() override {
    continue_loading_cb_.Run();
    delete this;
  }

  const base::Closure continue_loading_cb_;

  DISALLOW_COPY_AND_ASSIGN(MediaLoadDeferrer);
};

}  // namespace

ChromeContentRendererClient::ChromeContentRendererClient()
    : main_entry_time_(base::TimeTicks::Now()) {
#if defined(ENABLE_EXTENSIONS)
  extensions::ExtensionsClient::Set(
      extensions::ChromeExtensionsClient::GetInstance());
  extensions::ExtensionsRendererClient::Set(
      ChromeExtensionsRendererClient::GetInstance());
#endif
#if defined(ENABLE_PLUGINS)
  for (size_t i = 0; i < arraysize(kPredefinedAllowedCameraDeviceOrigins); ++i)
    allowed_camera_device_origins_.insert(
        kPredefinedAllowedCameraDeviceOrigins[i]);
  for (size_t i = 0; i < arraysize(kPredefinedAllowedCompositorOrigins); ++i)
    allowed_compositor_origins_.insert(kPredefinedAllowedCompositorOrigins[i]);
#endif
#if defined(ENABLE_PRINTING)
  printing::SetAgent(GetUserAgent());
#endif
}

ChromeContentRendererClient::~ChromeContentRendererClient() {
}

void ChromeContentRendererClient::RenderThreadStarted() {
  RenderThread* thread = RenderThread::Get();

  thread->Send(new StartupMetricHostMsg_RecordRendererMainEntryTime(
      main_entry_time_));

  chrome_observer_.reset(new ChromeRenderThreadObserver());
  web_cache_impl_.reset(new web_cache::WebCacheImpl());

#if defined(ENABLE_EXTENSIONS)
  ChromeExtensionsRendererClient::GetInstance()->RenderThreadStarted();
#endif

  prescient_networking_dispatcher_.reset(
      new network_hints::PrescientNetworkingDispatcher());
#if defined(ENABLE_SPELLCHECK)
  // ChromeRenderViewTest::SetUp() creates a Spellcheck and injects it using
  // SetSpellcheck(). Don't overwrite it.
  if (!spellcheck_) {
    spellcheck_.reset(new SpellCheck());
    thread->AddObserver(spellcheck_.get());
  }
#endif
  visited_link_slave_.reset(new visitedlink::VisitedLinkSlave());
#if defined(FULL_SAFE_BROWSING)
  phishing_classifier_.reset(safe_browsing::PhishingClassifierFilter::Create());
#endif
  prerender_dispatcher_.reset(new prerender::PrerenderDispatcher());
#if defined(ENABLE_WEBRTC)
  webrtc_logging_message_filter_ = new WebRtcLoggingMessageFilter(
      thread->GetIOMessageLoopProxy());
#endif

  thread->AddObserver(chrome_observer_.get());
#if defined(FULL_SAFE_BROWSING)
  thread->AddObserver(phishing_classifier_.get());
#endif
  thread->AddObserver(visited_link_slave_.get());
  thread->AddObserver(prerender_dispatcher_.get());
  thread->AddObserver(SearchBouncer::GetInstance());

#if defined(ENABLE_WEBRTC)
  thread->AddFilter(webrtc_logging_message_filter_.get());
#endif

  thread->RegisterExtension(extensions_v8::ExternalExtension::Get());
  thread->RegisterExtension(extensions_v8::LoadTimesExtension::Get());

  base::CommandLine* command_line = base::CommandLine::ForCurrentProcess();
  if (command_line->HasSwitch(switches::kEnableBenchmarking))
    thread->RegisterExtension(extensions_v8::BenchmarkingExtension::Get());
  if (command_line->HasSwitch(switches::kEnableNetBenchmarking))
    thread->RegisterExtension(extensions_v8::NetBenchmarkingExtension::Get());
  if (command_line->HasSwitch(switches::kInstantProcess))
    thread->RegisterExtension(extensions_v8::SearchBoxExtension::Get());

  // chrome-search: and chrome-distiller: pages  should not be accessible by
  // normal content, and should also be unable to script anything but themselves
  // (to help limit the damage that a corrupt page could cause).
  WebString chrome_search_scheme(ASCIIToUTF16(chrome::kChromeSearchScheme));

  // The Instant process can only display the content but not read it.  Other
  // processes can't display it or read it.
  if (!command_line->HasSwitch(switches::kInstantProcess))
    WebSecurityPolicy::registerURLSchemeAsDisplayIsolated(chrome_search_scheme);

  WebString dom_distiller_scheme(
      ASCIIToUTF16(dom_distiller::kDomDistillerScheme));
  // TODO(nyquist): Add test to ensure this happens when the flag is set.
  WebSecurityPolicy::registerURLSchemeAsDisplayIsolated(dom_distiller_scheme);

#if defined(OS_CHROMEOS)
  WebSecurityPolicy::registerURLSchemeAsLocal(
      WebString::fromUTF8(content::kExternalFileScheme));
#endif

#if defined(OS_ANDROID)
  WebSecurityPolicy::registerURLSchemeAsAllowedForReferrer(
      WebString::fromUTF8(chrome::kAndroidAppScheme));
#endif

#if defined(ENABLE_IPC_FUZZER)
  if (command_line->HasSwitch(switches::kIpcDumpDirectory)) {
    base::FilePath dump_directory =
        command_line->GetSwitchValuePath(switches::kIpcDumpDirectory);
    IPC::ChannelProxy::OutgoingMessageFilter* filter =
        LoadExternalIPCDumper(dump_directory);
    thread->GetChannel()->set_outgoing_message_filter(filter);
  }
#endif

  // chrome-search: pages should not be accessible by bookmarklets
  // or javascript: URLs typed in the omnibox.
  WebSecurityPolicy::registerURLSchemeAsNotAllowingJavascriptURLs(
      chrome_search_scheme);

  // chrome-search: resources shouldn't trigger insecure content warnings. Note
  // that chrome-extension: and chrome-extension-resource: schemes are taken
  // care of in extensions::Dispatcher.
  WebSecurityPolicy::registerURLSchemeAsSecure(chrome_search_scheme);

#if defined(ENABLE_PRINT_PREVIEW)
  pdf_print_client_.reset(new ChromePDFPrintClient());
  pdf::PepperPDFHost::SetPrintClient(pdf_print_client_.get());
#endif

  std::set<GURL> origins;
  GetSecureOriginWhitelist(&origins);
  for (const GURL& origin : origins) {
    WebSecurityPolicy::addOriginTrustworthyWhiteList(
        WebSecurityOrigin::create(origin));
  }

  std::set<std::string> schemes;
  GetSchemesBypassingSecureContextCheckWhitelist(&schemes);
  for (const std::string& scheme : schemes) {
    WebSecurityPolicy::addSchemeToBypassSecureContextWhitelist(
        WebString::fromUTF8(scheme));
  }
}

void ChromeContentRendererClient::RenderFrameCreated(
    content::RenderFrame* render_frame) {
  new ChromeRenderFrameObserver(render_frame);

  bool should_whitelist_for_content_settings =
      base::CommandLine::ForCurrentProcess()->HasSwitch(
          switches::kInstantProcess);
  extensions::Dispatcher* ext_dispatcher = NULL;
#if defined(ENABLE_EXTENSIONS)
  ext_dispatcher =
      ChromeExtensionsRendererClient::GetInstance()->extension_dispatcher();
#endif
  ContentSettingsObserver* content_settings = new ContentSettingsObserver(
      render_frame, ext_dispatcher, should_whitelist_for_content_settings);
  if (chrome_observer_.get()) {
    content_settings->SetContentSettingRules(
        chrome_observer_->content_setting_rules());
  }

#if defined(ENABLE_EXTENSIONS)
  ChromeExtensionsRendererClient::GetInstance()->RenderFrameCreated(
      render_frame);
#endif

#if defined(ENABLE_PLUGINS)
  new PepperHelper(render_frame);
#endif

#if !defined(DISABLE_NACL)
  new nacl::NaClHelper(render_frame);
#endif

#if defined(FULL_SAFE_BROWSING)
  safe_browsing::ThreatDOMDetails::Create(render_frame);
#endif

  new NetErrorHelper(render_frame);

  if (render_frame->IsMainFrame()) {
    // Only attach MainRenderFrameObserver to the main frame, since
    // we only want to log page load metrics for the main frame.
    new page_load_metrics::MetricsRenderFrameObserver(render_frame);
  } else {
    // Avoid any race conditions from having the browser tell subframes that
    // they're prerendering.
    if (prerender::PrerenderHelper::IsPrerendering(
            render_frame->GetRenderView()->GetMainRenderFrame())) {
      new prerender::PrerenderHelper(render_frame);
    }
  }

  // Set up a mojo service to test if this page is a distiller page.
  new dom_distiller::DistillerJsRenderFrameObserver(
      render_frame, chrome::ISOLATED_WORLD_ID_CHROME_INTERNAL);

  // Create DistillabilityAgent to send distillability updates to
  // DistillabilityDriver in the browser process.
  new dom_distiller::DistillabilityAgent(render_frame);

  // Set up a mojo service to test if this page is a contextual search page.
  new contextual_search::OverlayJsRenderFrameObserver(render_frame);

  PasswordAutofillAgent* password_autofill_agent =
      new PasswordAutofillAgent(render_frame);
  PasswordGenerationAgent* password_generation_agent =
      new PasswordGenerationAgent(render_frame, password_autofill_agent);
  new AutofillAgent(render_frame, password_autofill_agent,
                    password_generation_agent);
}

void ChromeContentRendererClient::RenderViewCreated(
    content::RenderView* render_view) {
#if defined(ENABLE_EXTENSIONS)
  ChromeExtensionsRendererClient::GetInstance()->RenderViewCreated(render_view);
#endif
  new PageLoadHistograms(render_view);
#if defined(ENABLE_PRINTING)
  new printing::PrintWebViewHelper(
      render_view, std::unique_ptr<printing::PrintWebViewHelper::Delegate>(
                       new ChromePrintWebViewHelperDelegate()));
#endif
#if defined(ENABLE_SPELLCHECK)
  new SpellCheckProvider(render_view, spellcheck_.get());
#endif
  new prerender::PrerendererClient(render_view);

  base::CommandLine* command_line = base::CommandLine::ForCurrentProcess();
  if (command_line->HasSwitch(switches::kInstantProcess))
    new SearchBox(render_view);

  new ChromeRenderViewObserver(render_view, web_cache_impl_.get());

  new password_manager::CredentialManagerClient(render_view);
}


SkBitmap* ChromeContentRendererClient::GetSadPluginBitmap() {
  return const_cast<SkBitmap*>(ResourceBundle::GetSharedInstance().
      GetImageNamed(IDR_SAD_PLUGIN).ToSkBitmap());
}

SkBitmap* ChromeContentRendererClient::GetSadWebViewBitmap() {
  return const_cast<SkBitmap*>(ResourceBundle::GetSharedInstance().
      GetImageNamed(IDR_SAD_WEBVIEW).ToSkBitmap());
}

bool ChromeContentRendererClient::OverrideCreatePlugin(
    content::RenderFrame* render_frame,
    WebLocalFrame* frame,
    const WebPluginParams& params,
    WebPlugin** plugin) {
  std::string orig_mime_type = params.mimeType.utf8();
#if defined(ENABLE_EXTENSIONS)
  if (!ChromeExtensionsRendererClient::GetInstance()->OverrideCreatePlugin(
          render_frame, params)) {
    return false;
  }
#endif

  GURL url(params.url);
#if defined(ENABLE_PLUGINS)
  ChromeViewHostMsg_GetPluginInfo_Output output;
  WebString top_origin = frame->top()->getSecurityOrigin().toString();
  render_frame->Send(new ChromeViewHostMsg_GetPluginInfo(
      render_frame->GetRoutingID(), url, blink::WebStringToGURL(top_origin),
      orig_mime_type, &output));
  *plugin = CreatePlugin(render_frame, frame, params, output);
#else  // !defined(ENABLE_PLUGINS)

#if defined(OS_ANDROID)
  if (plugins::MobileYouTubePlugin::IsYouTubeURL(url, orig_mime_type)) {
    base::StringPiece template_html(
        ResourceBundle::GetSharedInstance().GetRawDataResource(
            IDR_MOBILE_YOUTUBE_PLUGIN_HTML));
    *plugin = (new plugins::MobileYouTubePlugin(render_frame, frame, params,
                                                template_html))->plugin();
    return true;
  }
#endif  // defined(OS_ANDROID)

  PluginUMAReporter::GetInstance()->ReportPluginMissing(orig_mime_type, url);
  *plugin = NonLoadablePluginPlaceholder::CreateNotSupportedPlugin(
                render_frame, frame, params)->plugin();

#endif  // defined(ENABLE_PLUGINS)
  return true;
}

WebPlugin* ChromeContentRendererClient::CreatePluginReplacement(
    content::RenderFrame* render_frame,
    const base::FilePath& plugin_path) {
  return NonLoadablePluginPlaceholder::CreateErrorPlugin(render_frame,
                                                         plugin_path)->plugin();
}

void ChromeContentRendererClient::DeferMediaLoad(
    content::RenderFrame* render_frame,
    bool has_played_media_before,
    const base::Closure& closure) {
  // Don't allow autoplay/autoload of media resources in a RenderFrame that is
  // hidden and has never played any media before.  We want to allow future
  // loads even when hidden to allow playlist-like functionality.
  //
  // NOTE: This is also used to defer media loading for prerender.
  // NOTE: Switch can be used to allow autoplay, unless frame is prerendered.
  //
  // TODO(dalecurtis): Include an idle check too.  http://crbug.com/509135
  if ((render_frame->IsHidden() && !has_played_media_before &&
       !base::CommandLine::ForCurrentProcess()->HasSwitch(
           switches::kDisableGestureRequirementForMediaPlayback)) ||
      prerender::PrerenderHelper::IsPrerendering(render_frame)) {
    new MediaLoadDeferrer(render_frame, closure);
    return;
  }

  closure.Run();
}

#if defined(ENABLE_PLUGINS)
WebPlugin* ChromeContentRendererClient::CreatePlugin(
    content::RenderFrame* render_frame,
    WebLocalFrame* frame,
    const WebPluginParams& original_params,
    const ChromeViewHostMsg_GetPluginInfo_Output& output) {
  const WebPluginInfo& info = output.plugin;
  const std::string& actual_mime_type = output.actual_mime_type;
  const base::string16& group_name = output.group_name;
  const std::string& identifier = output.group_identifier;
  ChromeViewHostMsg_GetPluginInfo_Status status = output.status;
  GURL url(original_params.url);
  std::string orig_mime_type = original_params.mimeType.utf8();
  ChromePluginPlaceholder* placeholder = NULL;

  // If the browser plugin is to be enabled, this should be handled by the
  // renderer, so the code won't reach here due to the early exit in
  // OverrideCreatePlugin.
  if (status == ChromeViewHostMsg_GetPluginInfo_Status::kNotFound ||
      orig_mime_type == content::kBrowserPluginMimeType) {
    PluginUMAReporter::GetInstance()->ReportPluginMissing(orig_mime_type, url);
    placeholder = ChromePluginPlaceholder::CreateLoadableMissingPlugin(
        render_frame, frame, original_params);
  } else {
    // TODO(bauerb): This should be in content/.
    WebPluginParams params(original_params);
    for (size_t i = 0; i < info.mime_types.size(); ++i) {
      if (info.mime_types[i].mime_type == actual_mime_type) {
        AppendParams(info.mime_types[i].additional_param_names,
                     info.mime_types[i].additional_param_values,
                     &params.attributeNames, &params.attributeValues);
        break;
      }
    }
    if (params.mimeType.isNull() && (actual_mime_type.size() > 0)) {
      // Webkit might say that mime type is null while we already know the
      // actual mime type via ChromeViewHostMsg_GetPluginInfo. In that case
      // we should use what we know since WebpluginDelegateProxy does some
      // specific initializations based on this information.
      params.mimeType = WebString::fromUTF8(actual_mime_type.c_str());
    }

    ContentSettingsObserver* observer =
        ContentSettingsObserver::Get(render_frame);

    const ContentSettingsType content_type =
        ShouldUseJavaScriptSettingForPlugin(info)
            ? CONTENT_SETTINGS_TYPE_JAVASCRIPT
            : CONTENT_SETTINGS_TYPE_PLUGINS;

    if ((status == ChromeViewHostMsg_GetPluginInfo_Status::kUnauthorized ||
         status == ChromeViewHostMsg_GetPluginInfo_Status::kBlocked) &&
        observer->IsPluginTemporarilyAllowed(identifier)) {
      status = ChromeViewHostMsg_GetPluginInfo_Status::kAllowed;
    }

    auto create_blocked_plugin = [&render_frame, &frame, &params, &info,
                                  &identifier, &group_name](
        int template_id, const base::string16& message) {
      return ChromePluginPlaceholder::CreateBlockedPlugin(
          render_frame, frame, params, info, identifier, group_name,
          template_id, message, PowerSaverInfo());
    };
    switch (status) {
      case ChromeViewHostMsg_GetPluginInfo_Status::kNotFound: {
        NOTREACHED();
        break;
      }
      case ChromeViewHostMsg_GetPluginInfo_Status::kAllowed:
      case ChromeViewHostMsg_GetPluginInfo_Status::kPlayImportantContent: {
#if !defined(DISABLE_NACL) && defined(ENABLE_EXTENSIONS)
        const bool is_nacl_plugin =
            info.name == ASCIIToUTF16(nacl::kNaClPluginName);
        const bool is_nacl_mime_type =
            actual_mime_type == nacl::kNaClPluginMimeType;
        const bool is_pnacl_mime_type =
            actual_mime_type == nacl::kPnaclPluginMimeType;
        if (is_nacl_plugin || is_nacl_mime_type || is_pnacl_mime_type) {
          bool is_nacl_unrestricted = false;
          if (is_nacl_mime_type) {
            is_nacl_unrestricted =
                base::CommandLine::ForCurrentProcess()->HasSwitch(
                    switches::kEnableNaCl);
          } else if (is_pnacl_mime_type) {
            is_nacl_unrestricted = true;
          }
          GURL manifest_url;
          GURL app_url;
          if (is_nacl_mime_type || is_pnacl_mime_type) {
            // Normal NaCl/PNaCl embed. The app URL is the page URL.
            manifest_url = url;
            app_url = frame->top()->document().url();
          } else {
            // NaCl is being invoked as a content handler. Look up the NaCl
            // module using the MIME type. The app URL is the manifest URL.
            manifest_url = GetNaClContentHandlerURL(actual_mime_type, info);
            app_url = manifest_url;
          }
          const Extension* extension =
              extensions::RendererExtensionRegistry::Get()
                  ->GetExtensionOrAppByURL(manifest_url);
          if (!IsNaClAllowed(manifest_url,
                             app_url,
                             is_nacl_unrestricted,
                             extension,
                             &params)) {
            WebString error_message;
            if (is_nacl_mime_type) {
              error_message =
                  "Only unpacked extensions and apps installed from the Chrome "
                  "Web Store can load NaCl modules without enabling Native "
                  "Client in about:flags.";
            } else if (is_pnacl_mime_type) {
              error_message =
                  "Portable Native Client must not be disabled in about:flags.";
            }
            frame->addMessageToConsole(
                WebConsoleMessage(WebConsoleMessage::LevelError,
                                  error_message));
            placeholder = create_blocked_plugin(
                IDR_BLOCKED_PLUGIN_HTML,
#if defined(OS_CHROMEOS)
                l10n_util::GetStringUTF16(IDS_NACL_PLUGIN_BLOCKED));
#else
                l10n_util::GetStringFUTF16(IDS_PLUGIN_BLOCKED, group_name));
#endif
            break;
          }
        }
#endif  // !defined(DISABLE_NACL) && defined(ENABLE_EXTENSIONS)

        // Delay loading plugins if prerendering.
        // TODO(mmenke):  In the case of prerendering, feed into
        //                ChromeContentRendererClient::CreatePlugin instead, to
        //                reduce the chance of future regressions.
        bool is_prerendering =
            prerender::PrerenderHelper::IsPrerendering(render_frame);

        bool power_saver_setting_on =
            status ==
            ChromeViewHostMsg_GetPluginInfo_Status::kPlayImportantContent;
        PowerSaverInfo power_saver_info =
            PowerSaverInfo::Get(render_frame, power_saver_setting_on, params,
                                info, frame->document().url());
        if (power_saver_info.blocked_for_background_tab || is_prerendering ||
            !power_saver_info.poster_attribute.empty()) {
          placeholder = ChromePluginPlaceholder::CreateBlockedPlugin(
              render_frame, frame, params, info, identifier, group_name,
              power_saver_info.poster_attribute.empty()
                  ? IDR_BLOCKED_PLUGIN_HTML
                  : IDR_PLUGIN_POSTER_HTML,
              l10n_util::GetStringFUTF16(IDS_PLUGIN_BLOCKED, group_name),
              power_saver_info);
          placeholder->set_blocked_for_prerendering(is_prerendering);
          placeholder->AllowLoading();
          break;
        }

        std::unique_ptr<content::PluginInstanceThrottler> throttler;
        if (power_saver_info.power_saver_enabled) {
          throttler = PluginInstanceThrottler::Create();
          // PluginPreroller manages its own lifetime.
          new PluginPreroller(
              render_frame, frame, params, info, identifier, group_name,
              l10n_util::GetStringFUTF16(IDS_PLUGIN_BLOCKED, group_name),
              throttler.get());
        }

        return render_frame->CreatePlugin(frame, info, params,
                                          std::move(throttler));
      }
      case ChromeViewHostMsg_GetPluginInfo_Status::kDisabled: {
        PluginUMAReporter::GetInstance()->ReportPluginDisabled(orig_mime_type,
                                                               url);
        placeholder = create_blocked_plugin(
            IDR_DISABLED_PLUGIN_HTML,
            l10n_util::GetStringFUTF16(IDS_PLUGIN_DISABLED, group_name));
        break;
      }
      case ChromeViewHostMsg_GetPluginInfo_Status::kOutdatedBlocked: {
#if defined(ENABLE_PLUGIN_INSTALLATION)
        placeholder = create_blocked_plugin(
            IDR_BLOCKED_PLUGIN_HTML,
            l10n_util::GetStringFUTF16(IDS_PLUGIN_OUTDATED, group_name));
        placeholder->AllowLoading();
        render_frame->Send(new ChromeViewHostMsg_BlockedOutdatedPlugin(
            render_frame->GetRoutingID(), placeholder->CreateRoutingId(),
            identifier));
#else
        NOTREACHED();
#endif
        break;
      }
      case ChromeViewHostMsg_GetPluginInfo_Status::kOutdatedDisallowed: {
        placeholder = create_blocked_plugin(
            IDR_BLOCKED_PLUGIN_HTML,
            l10n_util::GetStringFUTF16(IDS_PLUGIN_OUTDATED, group_name));
        break;
      }
      case ChromeViewHostMsg_GetPluginInfo_Status::kUnauthorized: {
        placeholder = create_blocked_plugin(
            IDR_BLOCKED_PLUGIN_HTML,
            l10n_util::GetStringFUTF16(IDS_PLUGIN_NOT_AUTHORIZED, group_name));
        placeholder->AllowLoading();
        render_frame->Send(new ChromeViewHostMsg_BlockedUnauthorizedPlugin(
            render_frame->GetRoutingID(), group_name, identifier));
        observer->DidBlockContentType(content_type, group_name);
        break;
      }
      case ChromeViewHostMsg_GetPluginInfo_Status::kBlocked: {
        placeholder = create_blocked_plugin(
            IDR_BLOCKED_PLUGIN_HTML,
            l10n_util::GetStringFUTF16(IDS_PLUGIN_BLOCKED, group_name));
        placeholder->AllowLoading();
        RenderThread::Get()->RecordAction(UserMetricsAction("Plugin_Blocked"));
        observer->DidBlockContentType(content_type, group_name);
        break;
      }
      case ChromeViewHostMsg_GetPluginInfo_Status::kBlockedByPolicy: {
        placeholder = create_blocked_plugin(
            IDR_BLOCKED_PLUGIN_HTML,
            l10n_util::GetStringFUTF16(IDS_PLUGIN_BLOCKED_BY_POLICY,
                                       group_name));
        RenderThread::Get()->RecordAction(
            UserMetricsAction("Plugin_BlockedByPolicy"));
        observer->DidBlockContentType(content_type, group_name);
        break;
      }
    }
  }
  placeholder->SetStatus(status);
  return placeholder->plugin();
}
#endif  // defined(ENABLE_PLUGINS)

// For NaCl content handling plugins, the NaCl manifest is stored in an
// additonal 'nacl' param associated with the MIME type.
//  static
GURL ChromeContentRendererClient::GetNaClContentHandlerURL(
    const std::string& actual_mime_type,
    const content::WebPluginInfo& plugin) {
  // Look for the manifest URL among the MIME type's additonal parameters.
  const char kNaClPluginManifestAttribute[] = "nacl";
  base::string16 nacl_attr = ASCIIToUTF16(kNaClPluginManifestAttribute);
  for (size_t i = 0; i < plugin.mime_types.size(); ++i) {
    if (plugin.mime_types[i].mime_type == actual_mime_type) {
      const content::WebPluginMimeType& content_type = plugin.mime_types[i];
      for (size_t i = 0; i < content_type.additional_param_names.size(); ++i) {
        if (content_type.additional_param_names[i] == nacl_attr)
          return GURL(content_type.additional_param_values[i]);
      }
      break;
    }
  }
  return GURL();
}

#if !defined(DISABLE_NACL)
//  static
bool ChromeContentRendererClient::IsNaClAllowed(
    const GURL& manifest_url,
    const GURL& app_url,
    bool is_nacl_unrestricted,
    const Extension* extension,
    WebPluginParams* params) {
  // Temporarily allow these whitelisted apps and WebUIs to use NaCl.
  std::string app_url_host = app_url.host();
  std::string manifest_url_path = manifest_url.path();

  bool is_whitelisted_web_ui =
      app_url.spec() == chrome::kChromeUIAppListStartPageURL;

  bool is_photo_app =
      // Whitelisted apps must be served over https.
      app_url.SchemeIsCryptographic() && manifest_url.SchemeIsCryptographic() &&
      (base::EndsWith(app_url_host, "plus.google.com",
                      base::CompareCase::INSENSITIVE_ASCII) ||
       base::EndsWith(app_url_host, "plus.sandbox.google.com",
                      base::CompareCase::INSENSITIVE_ASCII)) &&
      manifest_url.DomainIs("ssl.gstatic.com") &&
      (manifest_url_path.find("s2/oz/nacl/") == 1 ||
       manifest_url_path.find("photos/nacl/") == 1);

  std::string manifest_fs_host;
  if (manifest_url.SchemeIsFileSystem() && manifest_url.inner_url()) {
    manifest_fs_host = manifest_url.inner_url()->host();
  }
  bool is_hangouts_app =
      // Whitelisted apps must be served over secure scheme.
      app_url.SchemeIsCryptographic() && manifest_url.SchemeIsFileSystem() &&
      manifest_url.inner_url()->SchemeIsCryptographic() &&
      (base::EndsWith(app_url_host, "talkgadget.google.com",
                      base::CompareCase::INSENSITIVE_ASCII) ||
       base::EndsWith(app_url_host, "plus.google.com",
                      base::CompareCase::INSENSITIVE_ASCII) ||
       base::EndsWith(app_url_host, "plus.sandbox.google.com",
                      base::CompareCase::INSENSITIVE_ASCII) ||
       base::EndsWith(app_url_host, "hangouts.google.com",
                      base::CompareCase::INSENSITIVE_ASCII)) &&
      // The manifest must be loaded from the host's FileSystem.
      (manifest_fs_host == app_url_host);

  bool is_whitelisted_app = is_photo_app || is_hangouts_app;

  bool is_invoked_by_webstore_installed_extension = false;
  bool is_extension_unrestricted = false;
  bool is_extension_force_installed = false;
#if defined(ENABLE_EXTENSIONS)
  bool is_extension_from_webstore = extension && extension->from_webstore();

  bool is_invoked_by_extension = app_url.SchemeIs("chrome-extension");
  bool is_invoked_by_hosted_app = extension &&
      extension->is_hosted_app() &&
      extension->web_extent().MatchesURL(app_url);

  is_invoked_by_webstore_installed_extension = is_extension_from_webstore &&
      (is_invoked_by_extension || is_invoked_by_hosted_app);

  // Allow built-in extensions and developer mode extensions.
  is_extension_unrestricted = extension &&
       (extensions::Manifest::IsUnpackedLocation(extension->location()) ||
        extensions::Manifest::IsComponentLocation(extension->location()));
  // Allow extensions force installed by admin policy.
  is_extension_force_installed = extension &&
       extensions::Manifest::IsPolicyLocation(extension->location());
#endif  // defined(ENABLE_EXTENSIONS)

  // Allow NaCl under any of the following circumstances:
  //  1) An app or URL is explictly whitelisted above.
  //  2) An extension is loaded unpacked or built-in (component) to Chrome.
  //  3) An extension is force installed by policy.
  //  4) An extension is installed from the webstore, and invoked in that
  //     context (hosted app URL or chrome-extension:// scheme).
  //  5) --enable-nacl is set.
  bool is_nacl_allowed_by_location =
      is_whitelisted_web_ui ||
      is_whitelisted_app ||
      is_extension_unrestricted ||
      is_extension_force_installed ||
      is_invoked_by_webstore_installed_extension;
  bool is_nacl_allowed = is_nacl_allowed_by_location || is_nacl_unrestricted;
  if (is_nacl_allowed) {
    // Make sure that PPAPI 'dev' interfaces are only available for unpacked
    // and component extensions.  Also allow dev interfaces when --enable-nacl
    // is set, but do not allow --enable-nacl to provide dev interfaces to
    // webstore installed and other normally allowed URLs.
    WebString dev_attribute = WebString::fromUTF8("@dev");
    if (is_extension_unrestricted ||
        (is_nacl_unrestricted && !is_nacl_allowed_by_location)) {
      // Add the special '@dev' attribute.
      std::vector<base::string16> param_names;
      std::vector<base::string16> param_values;
      param_names.push_back(dev_attribute);
      param_values.push_back(WebString());
      AppendParams(
          param_names,
          param_values,
          &params->attributeNames,
          &params->attributeValues);
    } else {
      // If the params somehow contain '@dev', remove it.
      size_t attribute_count = params->attributeNames.size();
      for (size_t i = 0; i < attribute_count; ++i) {
        if (params->attributeNames[i].equals(dev_attribute))
          params->attributeNames[i] = WebString();
      }
    }
  }
  return is_nacl_allowed;
}
#endif  // defined(DISABLE_NACL)

bool ChromeContentRendererClient::HasErrorPage(int http_status_code,
                                               std::string* error_domain) {
  // Use an internal error page, if we have one for the status code.
  if (!error_page::LocalizedError::HasStrings(
          error_page::LocalizedError::kHttpErrorDomain, http_status_code)) {
    return false;
  }

  *error_domain = error_page::LocalizedError::kHttpErrorDomain;
  return true;
}

bool ChromeContentRendererClient::ShouldSuppressErrorPage(
    content::RenderFrame* render_frame,
    const GURL& url) {
  // Unit tests for ChromeContentRendererClient pass a NULL RenderFrame here.
  // Unfortunately it's very difficult to construct a mock RenderView, so skip
  // this functionality in this case.
  if (render_frame &&
      NetErrorHelper::Get(render_frame)->ShouldSuppressErrorPage(url)) {
    return true;
  }
  // Do not flash an error page if the Instant new tab page fails to load.
  return SearchBouncer::GetInstance()->IsNewTabPage(url);
}

void ChromeContentRendererClient::GetNavigationErrorStrings(
    content::RenderFrame* render_frame,
    const WebURLRequest& failed_request,
    const WebURLError& error,
    std::string* error_html,
    base::string16* error_description) {
  const GURL failed_url = error.unreachableURL;

  bool is_post = base::EqualsASCII(
      base::StringPiece16(failed_request.httpMethod()), "POST");
  bool is_ignoring_cache =
      failed_request.getCachePolicy() == WebCachePolicy::BypassingCache;
  if (error_html) {
    NetErrorHelper::Get(render_frame)
        ->GetErrorHTML(error, is_post, is_ignoring_cache, error_html);
  }

  if (error_description) {
    *error_description = error_page::LocalizedError::GetErrorDetails(
        error.domain.utf8(), error.reason, is_post);
  }
}

bool ChromeContentRendererClient::RunIdleHandlerWhenWidgetsHidden() {
#if defined(ENABLE_EXTENSIONS)
  return !IsStandaloneExtensionProcess();
#else
  return true;
#endif
}

bool ChromeContentRendererClient::
    AllowTimerSuspensionWhenProcessBackgrounded() {
#if defined(OS_ANDROID)
  return true;
#else
  return false;
#endif
}

bool ChromeContentRendererClient::AllowPopup() {
#if defined(ENABLE_EXTENSIONS)
  return ChromeExtensionsRendererClient::GetInstance()->AllowPopup();
#else
  return false;
#endif
}

bool ChromeContentRendererClient::ShouldFork(WebLocalFrame* frame,
                                             const GURL& url,
                                             const std::string& http_method,
                                             bool is_initial_navigation,
                                             bool is_server_redirect,
                                             bool* send_referrer) {
  DCHECK(!frame->parent());

  // If this is the Instant process, fork all navigations originating from the
  // renderer.  The destination page will then be bucketed back to this Instant
  // process if it is an Instant url, or to another process if not.  Conversely,
  // fork if this is a non-Instant process navigating to an Instant url, so that
  // such navigations can also be bucketed into an Instant renderer.
  if (base::CommandLine::ForCurrentProcess()->HasSwitch(
          switches::kInstantProcess) ||
      SearchBouncer::GetInstance()->ShouldFork(url)) {
    *send_referrer = true;
    return true;
  }

  // For now, we skip the rest for POST submissions.  This is because
  // http://crbug.com/101395 is more likely to cause compatibility issues
  // with hosted apps and extensions than WebUI pages.  We will remove this
  // check when cross-process POST submissions are supported.
  if (http_method != "GET")
    return false;

  // If |url| matches one of the prerendered URLs, stop this navigation and try
  // to swap in the prerendered page on the browser process. If the prerendered
  // page no longer exists by the time the OpenURL IPC is handled, a normal
  // navigation is attempted.
  if (prerender_dispatcher_.get() &&
      prerender_dispatcher_->IsPrerenderURL(url)) {
    *send_referrer = true;
    return true;
  }

#if defined(ENABLE_EXTENSIONS)
  bool should_fork = ChromeExtensionsRendererClient::ShouldFork(
      frame, url, is_initial_navigation, is_server_redirect, send_referrer);
  if (should_fork)
    return true;
#endif  // defined(ENABLE_EXTENSIONS)

  return false;
}

bool ChromeContentRendererClient::WillSendRequest(
    WebFrame* frame,
    ui::PageTransition transition_type,
    const GURL& url,
    const GURL& first_party_for_cookies,
    GURL* new_url) {
  // Check whether the request should be allowed. If not allowed, we reset the
  // URL to something invalid to prevent the request and cause an error.
#if defined(ENABLE_EXTENSIONS)
  if (ChromeExtensionsRendererClient::GetInstance()->WillSendRequest(
          frame, transition_type, url, new_url)) {
    return true;
  }
#endif

  const content::RenderView* render_view =
      content::RenderView::FromWebView(frame->view());
  SearchBox* search_box = SearchBox::Get(render_view);
  if (search_box && url.SchemeIs(chrome::kChromeSearchScheme)) {
    SearchBox::ImageSourceType type = SearchBox::NONE;
    if (url.host() == chrome::kChromeUIFaviconHost)
      type = SearchBox::FAVICON;
    else if (url.host() == chrome::kChromeUILargeIconHost)
      type = SearchBox::LARGE_ICON;
    else if (url.host() == chrome::kChromeUIFallbackIconHost)
      type = SearchBox::FALLBACK_ICON;
    else if (url.host() == chrome::kChromeUIThumbnailHost)
      type = SearchBox::THUMB;

    if (type != SearchBox::NONE)
      return search_box->GenerateImageURLFromTransientURL(url, type, new_url);
  }

  return false;
}

unsigned long long ChromeContentRendererClient::VisitedLinkHash(
    const char* canonical_url, size_t length) {
  return visited_link_slave_->ComputeURLFingerprint(canonical_url, length);
}

bool ChromeContentRendererClient::IsLinkVisited(unsigned long long link_hash) {
  return visited_link_slave_->IsVisited(link_hash);
}

blink::WebPrescientNetworking*
ChromeContentRendererClient::GetPrescientNetworking() {
  return prescient_networking_dispatcher_.get();
}

bool ChromeContentRendererClient::ShouldOverridePageVisibilityState(
    const content::RenderFrame* render_frame,
    blink::WebPageVisibilityState* override_state) {
  if (!prerender::PrerenderHelper::IsPrerendering(render_frame))
    return false;

  *override_state = blink::WebPageVisibilityStatePrerender;
  return true;
}

#if defined(ENABLE_SPELLCHECK)
void ChromeContentRendererClient::SetSpellcheck(SpellCheck* spellcheck) {
  RenderThread* thread = RenderThread::Get();
  if (spellcheck_.get() && thread)
    thread->RemoveObserver(spellcheck_.get());
  spellcheck_.reset(spellcheck);
  SpellCheckReplacer replacer(spellcheck_.get());
  content::RenderView::ForEach(&replacer);
  if (thread)
    thread->AddObserver(spellcheck_.get());
}
#endif

bool ChromeContentRendererClient::IsExternalPepperPlugin(
    const std::string& module_name) {
  // TODO(bbudge) remove this when the trusted NaCl plugin has been removed.
  // We must defer certain plugin events for NaCl instances since we switch
  // from the in-process to the out-of-process proxy after instantiating them.
  return module_name == "Native Client";
}

#if defined(ENABLE_PLUGINS) && defined(ENABLE_EXTENSIONS)
bool ChromeContentRendererClient::IsExtensionOrSharedModuleWhitelisted(
    const GURL& url, const std::set<std::string>& whitelist) {
  const extensions::ExtensionSet* extension_set =
      extensions::RendererExtensionRegistry::Get()->GetMainThreadExtensionSet();
  return chrome::IsExtensionOrSharedModuleWhitelisted(url, extension_set,
      whitelist);
}
#endif

blink::WebSpeechSynthesizer*
ChromeContentRendererClient::OverrideSpeechSynthesizer(
    blink::WebSpeechSynthesizerClient* client) {
  return new TtsDispatcher(client);
}

bool ChromeContentRendererClient::AllowPepperMediaStreamAPI(
    const GURL& url) {
#if !defined(OS_ANDROID)
  // Allow only the Hangouts app to use the MediaStream APIs. It's OK to check
  // the whitelist in the renderer, since we're only preventing access until
  // these APIs are public and stable.
  std::string url_host = url.host();
  if (url.SchemeIs("https") &&
      (base::EndsWith(url_host, "talkgadget.google.com",
                      base::CompareCase::INSENSITIVE_ASCII) ||
       base::EndsWith(url_host, "plus.google.com",
                      base::CompareCase::INSENSITIVE_ASCII) ||
       base::EndsWith(url_host, "plus.sandbox.google.com",
                      base::CompareCase::INSENSITIVE_ASCII)) &&
      base::StartsWith(url.path(), "/hangouts/",
                       base::CompareCase::INSENSITIVE_ASCII)) {
    return true;
  }
  // Allow access for tests.
  if (base::CommandLine::ForCurrentProcess()->HasSwitch(
          switches::kEnablePepperTesting)) {
    return true;
  }
#endif  // !defined(OS_ANDROID)
  return false;
}

void ChromeContentRendererClient::AddSupportedKeySystems(
    std::vector<std::unique_ptr<::media::KeySystemProperties>>* key_systems) {
  AddChromeKeySystems(key_systems);
}

bool ChromeContentRendererClient::ShouldReportDetailedMessageForSource(
    const base::string16& source) const {
#if defined(ENABLE_EXTENSIONS)
  return extensions::IsSourceFromAnExtension(source);
#else
  return false;
#endif
}

bool ChromeContentRendererClient::ShouldGatherSiteIsolationStats() const {
  // Site isolation stats are gathered currently for non-extension renderer
  // processes running a normal web page from the Internet.
  // TODO(nick): https://crbug.com/268640 Gather stats for extension processes
  // too; we would need to check the extension's manifest to know which sites
  // it's allowed to access.
#if defined(ENABLE_EXTENSIONS)
  base::CommandLine* command_line = base::CommandLine::ForCurrentProcess();
  return !command_line->HasSwitch(extensions::switches::kExtensionProcess);
#else
  return true;
#endif
}

blink::WebWorkerContentSettingsClientProxy*
ChromeContentRendererClient::CreateWorkerContentSettingsClientProxy(
    content::RenderFrame* render_frame,
    WebFrame* frame) {
  return new WorkerContentSettingsClientProxy(render_frame, frame);
}

bool ChromeContentRendererClient::IsPluginAllowedToUseDevChannelAPIs() {
#if defined(ENABLE_PLUGINS)
  // Allow access for tests.
  if (base::CommandLine::ForCurrentProcess()->HasSwitch(
          switches::kEnablePepperTesting)) {
    return true;
  }

  version_info::Channel channel = chrome::GetChannel();
  // Allow dev channel APIs to be used on "Canary", "Dev", and "Unknown"
  // releases of Chrome. Permitting "Unknown" allows these APIs to be used on
  // Chromium builds as well.
  return channel <= version_info::Channel::DEV;
#else
  return false;
#endif
}

bool ChromeContentRendererClient::IsPluginAllowedToUseCameraDeviceAPI(
    const GURL& url) {
#if defined(ENABLE_PLUGINS) && defined(ENABLE_EXTENSIONS)
  if (base::CommandLine::ForCurrentProcess()->HasSwitch(
          switches::kEnablePepperTesting))
    return true;

  if (IsExtensionOrSharedModuleWhitelisted(url, allowed_camera_device_origins_))
    return true;
#endif

  return false;
}

bool ChromeContentRendererClient::IsPluginAllowedToUseCompositorAPI(
    const GURL& url) {
#if defined(ENABLE_PLUGINS) && defined(ENABLE_EXTENSIONS)
  if (base::CommandLine::ForCurrentProcess()->HasSwitch(
          switches::kEnablePepperTesting))
    return true;
  if (IsExtensionOrSharedModuleWhitelisted(url, allowed_compositor_origins_))
    return true;

  version_info::Channel channel = chrome::GetChannel();
  return channel <= version_info::Channel::DEV;
#else
  return false;
#endif
}

content::BrowserPluginDelegate*
ChromeContentRendererClient::CreateBrowserPluginDelegate(
    content::RenderFrame* render_frame,
    const std::string& mime_type,
    const GURL& original_url) {
#if defined(ENABLE_EXTENSIONS)
  return ChromeExtensionsRendererClient::CreateBrowserPluginDelegate(
    render_frame, mime_type, original_url);
#else
  return nullptr;
#endif
}

void ChromeContentRendererClient::RecordRappor(const std::string& metric,
                                               const std::string& sample) {
  RenderThread::Get()->Send(new ChromeViewHostMsg_RecordRappor(metric, sample));
}

void ChromeContentRendererClient::RecordRapporURL(const std::string& metric,
                                                  const GURL& url) {
  RenderThread::Get()->Send(new ChromeViewHostMsg_RecordRapporURL(metric, url));
}

std::unique_ptr<blink::WebAppBannerClient>
ChromeContentRendererClient::CreateAppBannerClient(
    content::RenderFrame* render_frame) {
  return std::unique_ptr<blink::WebAppBannerClient>(
      new AppBannerClient(render_frame));
}

void ChromeContentRendererClient::AddImageContextMenuProperties(
    const WebURLResponse& response,
    std::map<std::string, std::string>* properties) {
  DCHECK(properties);
  WebString header_key(ASCIIToUTF16(
      data_reduction_proxy::chrome_proxy_header()));
  if (!response.httpHeaderField(header_key).isNull() &&
      response.httpHeaderField(header_key).utf8().find(
          data_reduction_proxy::chrome_proxy_lo_fi_directive()) !=
              std::string::npos) {
    (*properties)[data_reduction_proxy::chrome_proxy_header()] =
        data_reduction_proxy::chrome_proxy_lo_fi_directive();
  }
}

void ChromeContentRendererClient::RunScriptsAtDocumentStart(
    content::RenderFrame* render_frame) {
#if defined(ENABLE_EXTENSIONS)
  ChromeExtensionsRendererClient::GetInstance()->RunScriptsAtDocumentStart(
      render_frame);
  // |render_frame| might be dead by now.
#endif
}

void ChromeContentRendererClient::RunScriptsAtDocumentEnd(
    content::RenderFrame* render_frame) {
#if defined(ENABLE_EXTENSIONS)
  ChromeExtensionsRendererClient::GetInstance()->RunScriptsAtDocumentEnd(
      render_frame);
  // |render_frame| might be dead by now.
#endif
}

void
ChromeContentRendererClient::DidInitializeServiceWorkerContextOnWorkerThread(
    v8::Local<v8::Context> context,
    const GURL& url) {
#if defined(ENABLE_EXTENSIONS)
  extensions::Dispatcher::DidInitializeServiceWorkerContextOnWorkerThread(
      context, url);
#endif
}

void ChromeContentRendererClient::WillDestroyServiceWorkerContextOnWorkerThread(
    v8::Local<v8::Context> context,
    const GURL& url) {
#if defined(ENABLE_EXTENSIONS)
  extensions::Dispatcher::WillDestroyServiceWorkerContextOnWorkerThread(context,
                                                                        url);
#endif
}

// If we're in an extension, there is no need disabling multiple routes as
// chrome.system.network.getNetworkInterfaces provides the same
// information. Also, the enforcement of sending and binding UDP is already done
// by chrome extension permission model.
bool ChromeContentRendererClient::ShouldEnforceWebRTCRoutingPreferences() {
#if defined(ENABLE_EXTENSIONS)
  return !IsStandaloneExtensionProcess();
#else
  return true;
#endif
}
