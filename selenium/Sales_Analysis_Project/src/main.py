import sys
import logging
from pathlib import Path

# 2️⃣ ضبط المسارات (عشان الـ Imports تشتغل)
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent  # يرجع خطوة لفوق (من src إلى المشروع الرئيسي)
sys.path.insert(0, str(project_root))

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

from config.settings import INPUT_FILE, IMAGES_DIR, REPORTS_DIR, CHART_CONFIG, REQUIRED_COLUMNS
from core.loader import DataLoader
from core.analyzer import SalesAnalyzer
from core.visualizer import ChartGenerator
from core.reporter import ReportExporter


def main():
    logger.info("🚀 بدء تحليل المبيعات...")

    try:
        # 1️⃣ تحميل وتنظيف البيانات
        logger.info("📂 جاري تحميل البيانات...")
        loader = DataLoader(INPUT_FILE)
        df = loader.load().clean(REQUIRED_COLUMNS)

        # 2️⃣ التحليل
        logger.info("📊 جاري التحليل...")
        analyzer = SalesAnalyzer(df)
        region_data = analyzer.by_region()
        product_data = analyzer.by_product()
        trend_data = analyzer.by_date()
        kpis = analyzer.get_kpis()

        # 3️⃣ إنشاء الرسوم
        logger.info("📈 جاري إنشاء الرسوم البيانية...")
        visualizer = ChartGenerator(IMAGES_DIR, CHART_CONFIG)
        visualizer.bar_by_region(region_data)
        visualizer.barh_by_product(product_data)
        visualizer.line_trend(trend_data)

        # 4️⃣ تصدير التقارير
        logger.info("💾 جاري تصدير التقارير...")
        exporter = ReportExporter(REPORTS_DIR)

        exporter.to_excel({
            'Clean_Data': df,
            'By_Region': region_data,
            'By_Product': product_data,
            'Trend': trend_data
        })

        exporter.to_pdf_simple(kpis, region_data)

        # 5️⃣ الخلاصة
        logger.info("\n" + "=" * 50)
        logger.info("🎉 انتهى التحليل بنجاح!")
        logger.info(f"📁 المخرجات في: {REPORTS_DIR}")
        logger.info("=" * 50)

    except FileNotFoundError as e:
        logger.error(f"❌ الملف غير موجود: {e}")
    except Exception as e:
        logger.error(f"❌ خطأ غير متوقع: {e}")
        raise


if __name__ == "__main__":
    main()