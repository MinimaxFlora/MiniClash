import 'package:miniclash/common/common.dart';
import 'package:miniclash/enum/enum.dart';
import 'package:miniclash/icons/icons.dart';
import 'package:miniclash/providers/app.dart';
import 'package:miniclash/views/dns_queries.dart';
import 'package:miniclash/widgets/widgets.dart';
import 'package:material_ui/material_ui.dart';

import 'feed_card.dart';

class DnsQueriesCard extends StatelessWidget {
  const DnsQueriesCard({super.key});

  void _openDnsQueries(BuildContext context) {
    showSnapSheet(
      context,
      initialScrollOffset: double.maxFinite,
      builder: (_, controller) => NestedPagedSheet(
        builder: (_) => DnsQueriesView(scrollController: controller),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return FeedCard(
      label: PageLabel.dns.label,
      glyph: AppGlyphs.dns,
      onPressed: () => _openDnsQueries(context),
      child: ThrottledFeedCount(provider: dnsQueryCountProvider),
    );
  }
}
