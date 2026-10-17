import 'package:miniclash/common/common.dart';
import 'package:miniclash/icons/icons.dart';
import 'package:miniclash/providers/app.dart';
import 'package:miniclash/state.dart';
import 'package:miniclash/views/dashboard/widget_metrics.dart';
import 'package:miniclash/widgets/widgets.dart';
import 'package:material_ui/material_ui.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class RunTimeCard extends StatelessWidget {
  const RunTimeCard({super.key});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: DashboardWidgetMetrics.heightOf(context, 1),
      child: CommonCard(
        radius: DashboardWidgetMetrics.radiusOf(context),
        infoPadding: DashboardWidgetMetrics.paddingOf(
          context,
        ).copyWith(bottom: 0),
        info: Info(
          label: context.appLocalizations.runTime,
          glyph: AppGlyphs.history,
        ),
        onPressed: () {},
        child: Container(
          padding: DashboardWidgetMetrics.paddingOf(context).copyWith(top: 0),
          child: Column(
            mainAxisSize: MainAxisSize.max,
            mainAxisAlignment: MainAxisAlignment.end,
            children: [
              SizedBox(
                height:
                    globalState.measure.bodyMediumHeight *
                        DashboardWidgetMetrics.textScaleOf(context) +
                    2,
                child: Consumer(
                  builder: (_, ref, _) {
                    return Align(
                      alignment: Alignment.centerLeft,
                      child: Text(
                        getTimeText(ref.watch(runTimeProvider)),
                        style: context.textTheme.bodyMedium?.toLight
                            .adjustSize(1)
                            .copyWith(
                              fontFeatures: const [
                                FontFeature.tabularFigures(),
                              ],
                            ),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                    );
                  },
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
