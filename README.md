# System Monitor Application

## English

### Overview
The **System Monitor** application is a robust and user-friendly desktop tool developed using Python and PyQt6, designed to provide real-time monitoring of system resources such as CPU, RAM, and disk usage. It features a sleek interface with customizable themes and multilingual support, offering an intuitive way for technical users to track system performance. The application includes dynamic graphs, detailed resource statistics, and a history log for analyzing usage trends over time.

### Features
- **Real-Time Monitoring**: Displays live CPU, RAM, and disk usage percentages with progress bars and graphs.
- **Dynamic Graphs**: Visualizes resource usage trends over time using Matplotlib-powered line graphs.
- **Customizable Interface**: Supports multiple themes (Windows11, Dark, Light, Red, Blue) and languages (English, Persian, Chinese, Russian).
- **Warning System**: Alerts users when resource usage exceeds a configurable threshold (default: 80%).
- **History Tracking**: Logs resource usage with timestamps, savable to a JSON file for further analysis.
- **Detailed Statistics**: Provides comprehensive details such as total, used, and free memory/disk space, and CPU core counts.

### Requirements
- Python 3.9 or higher
- PyQt6
- psutil
- matplotlib
- numpy

### Installation
1. Ensure Python 3.9+ is installed on your system.
2. Install the required packages:
   ```bash
   pip install PyQt6 psutil matplotlib numpy
   ```
3. Download the application source code from the repository.
4. Run the application:
   ```bash
   python system_monitor.py
   ```

### Usage
- **System Monitor Tab**: View real-time CPU, RAM, and disk usage with progress bars, graphs, and detailed statistics.
- **History Tab**: Review logged resource usage data and save it to a JSON file for record-keeping.
- **Settings Tab**: Customize the language, theme, refresh rate (in milliseconds), and warning threshold for resource usage alerts.
- **Themes**: Choose from Windows11, Dark, Light, Red, or Blue themes for a personalized look.
- **Languages**: Switch between English, Persian, Chinese, and Russian, with proper text alignment (right-to-left for Persian).

### Contributing
Contributions are welcome! Feel free to submit issues or pull requests to enhance the application.

### License
This project is licensed under the MIT License.

---

## فارسی

### بررسی اجمالی
برنامه **مانیتور سیستم** یک ابزار دسکتاپ قدرتمند و کاربرپسند است که با استفاده از پایتون و PyQt6 توسعه یافته و برای نظارت لحظه‌ای بر منابع سیستم مانند CPU، RAM و دیسک طراحی شده است. این برنامه دارای رابط کاربری زیبا با تم‌های قابل‌تنظیم و پشتیبانی از چند زبان است که راهی بصری برای کاربران فنی جهت ردیابی عملکرد سیستم ارائه می‌دهد. این اپلیکیشن شامل نمودارهای پویا، آمار دقیق منابع و لاگ تاریخچه برای تحلیل روندهای استفاده در طول زمان است.

### ویژگی‌ها
- **نظارت لحظه‌ای**: نمایش درصد استفاده از CPU، RAM و دیسک به‌صورت زنده با نوارهای پیشرفت و نمودارها.
- **نمودارهای پویا**: نمایش روند استفاده از منابع با استفاده از نمودارهای خطی مبتنی بر Matplotlib.
- **رابط کاربری قابل‌تنظیم**: پشتیبانی از تم‌های متعدد (ویندوز ۱۱، تیره، روشن، قرمز، آبی) و زبان‌ها (انگلیسی، فارسی، چینی، روسی).
- **سیستم هشدار**: هشدار به کاربران در صورت عبور استفاده از منابع از آستانه قابل‌تنظیم (پیش‌فرض: ۸۰٪).
- **پیگیری تاریخچه**: ثبت داده‌های استفاده از منابع با زمان‌بندی، قابل ذخیره در فایل JSON برای تحلیل بیشتر.
- **آمار دقیق**: ارائه جزئیات جامع مانند کل، استفاده‌شده و فضای آزاد حافظه/دیسک و تعداد هسته‌های CPU.

### پیش‌نیازها
- پایتون ۳.۹ یا بالاتر
- PyQt6
- psutil
- matplotlib
- numpy

### نصب
۱. اطمینان حاصل کنید که پایتون ۳.۹ یا بالاتر روی سیستم شما نصب است.
۲. بسته‌های موردنیاز را نصب کنید:
   ```bash
   pip install PyQt6 psutil matplotlib numpy
   ```
۳. کد منبع برنامه را از مخزن دانلود کنید.
۴. برنامه را اجرا کنید:
   ```bash
   python system_monitor.py
   ```

### استفاده
- **تب مانیتور سیستم**: مشاهده استفاده لحظه‌ای از CPU، RAM و دیسک با نوارهای پیشرفت، نمودارها و آمار دقیق.
- **تب تاریخچه**: بررسی داده‌های ثبت‌شده استفاده از منابع و ذخیره آن‌ها در فایل JSON برای نگهداری سوابق.
- **تب تنظیمات**: شخصی‌سازی زبان، تم، نرخ به‌روزرسانی (به میلی‌ثانیه) و آستانه هشدار برای اعلان‌های استفاده از منابع.
- **تم‌ها**: انتخاب از میان تم‌های ویندوز ۱۱، تیره، روشن، قرمز یا آبی برای ظاهری شخصی‌سازی‌شده.
- **زبان‌ها**: جابجایی بین انگلیسی، فارسی، چینی و روسی با تراز متن مناسب (راست‌چین برای فارسی).

### مشارکت
از مشارکت استقبال می‌شود! لطفاً برای بهبود برنامه، مشکلات را گزارش دهید یا درخواست‌های pull ارسال کنید.

### مجوز
این پروژه تحت مجوز MIT منتشر شده است.

---

## 中文

### 概述
**系统监控器**应用程序是一款功能强大且用户友好的桌面工具，使用Python和PyQt6开发，旨在实时监控CPU、内存和磁盘等系统资源的使用情况。它拥有优雅的界面，支持可定制主题和多语言，为技术用户提供直观的系统性能跟踪方式。该应用程序包括动态图表、详细的资源统计信息以及历史记录日志，用于分析资源使用趋势。

### 功能
- **实时监控**：通过进度条和图表实时显示CPU、内存和磁盘使用百分比。
- **动态图表**：使用基于Matplotlib的折线图可视化资源使用趋势。
- **可定制界面**：支持多种主题（Windows11、暗色、亮色、红色、蓝色）和语言（英语、波斯语、汉语、俄语）。
- **警告系统**：当资源使用量超过可配置阈值（默认：80%）时提醒用户。
- **历史记录**：记录带有时间戳的资源使用数据，可保存为JSON文件以供进一步分析。
- **详细统计**：提供全面的详细信息，如总计、已使用和可用内存/磁盘空间，以及CPU核心数量。

### 要求
- Python 3.9 或更高版本
- PyQt6
- psutil
- matplotlib
- numpy

### 安装
1. 确保系统中已安装Python 3.9或更高版本。
2. 安装所需包：
   ```bash
   pip install PyQt6 psutil matplotlib numpy
   ```
3. 从仓库下载应用程序源代码。
4. 运行应用程序：
   ```bash
   python system_monitor.py
   ```

### 使用方法
- **系统监控选项卡**：通过进度条、图表和详细统计信息查看CPU、内存和磁盘的实时使用情况。
- **历史记录选项卡**：查看记录的资源使用数据并将其保存为JSON文件以便存档。
- **设置选项卡**：自定义语言、主题、刷新率（以毫秒为单位）以及资源使用警告阈值。
- **主题**：从Windows11、暗色、亮色、红色或蓝色主题中选择，打造个性化外观。
- **语言**：在英语、波斯语、汉语和俄语之间切换，支持适当的文本对齐（波斯语为右对齐）。

### 贡献
欢迎贡献！请提交问题或拉取请求以改进应用程序。

### 许可证
本项目采用MIT许可证。