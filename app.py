from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import matplotlib

matplotlib.use('Agg')

app = Flask(__name__)

def group_top_n(series, n=5):
    top_n = series.nlargest(n)
    others = series[~series.index.isin(top_n.index)].sum()
    grouped_series = pd.concat([top_n, pd.Series({'Others': others})])
    return grouped_series

@app.route('/')
def index():
    # CSVファイルの読み込み
    df = pd.read_csv('aa.csv')  # 'data.csv'をCSVファイルのパスに置き換えてください

    # TLDの集計
    tld_counts = df['top_level_domain'].value_counts()
    tld_counts = group_top_n(tld_counts, 5)  # 上位5つとその他をグループ化

    # 円グラフの作成 (TLD)
    fig, ax = plt.subplots()
    tld_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90, cmap='Pastel1')
    ax.set_ylabel('')
    ax.set_title('Top 5 Level Domain Distribution')

    # グラフを画像に変換
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    tld_plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    # プロトコルの集計
    protocol_counts = df['protocol_type'].value_counts()

    # 円グラフの作成 (Protocol Type)
    fig, ax = plt.subplots()
    protocol_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90, colors=['#66b3ff','#99ff99'])
    ax.set_ylabel('')
    ax.set_title('Protocol Type Distribution')

    # グラフを画像に変換
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    protocol_plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    # 棒グラフの作成 (TLD)
    fig, ax = plt.subplots()
    tld_counts.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_ylabel('Count')
    ax.set_title('Top 5 Level Domain Distribution (Bar)')

    # グラフを画像に変換
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    tld_bar_plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    # 棒グラフの作成 (Protocol Type)
    fig, ax = plt.subplots()
    protocol_counts.plot(kind='bar', ax=ax, color='lightgreen')
    ax.set_ylabel('Count')
    ax.set_title('Protocol Type Distribution (Bar)')

    # グラフを画像に変換
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    protocol_bar_plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    # newgTLDの割合計算と円グラフ作成
    newgTLD_count = df['newgTLD'].sum()
    total_count = len(df)
    newgTLD_percentage = (newgTLD_count / total_count) * 100

    # newgTLDの円グラフ作成
    labels = ['newgTLD', 'Not newgTLD']
    sizes = [newgTLD_count, total_count - newgTLD_count]
    colors = ['#ff9999','#66b3ff']

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    ax.set_title('Distribution of newgTLD vs Non-newgTLD')

    # グラフを画像に変換
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    newgTLD_plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('index.html', 
                           tld_plot_url=tld_plot_url, 
                           protocol_plot_url=protocol_plot_url, 
                           tld_bar_plot_url=tld_bar_plot_url, 
                           protocol_bar_plot_url=protocol_bar_plot_url,
                           newgTLD_percentage=newgTLD_percentage,
                           newgTLD_plot_url=newgTLD_plot_url)

if __name__ == '__main__':
    app.run(debug=True)
