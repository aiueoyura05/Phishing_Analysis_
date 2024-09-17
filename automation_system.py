import pandas as pd
import time

class DataAnalyzer:
    def __init__(self, filename):
        # 'From' カラムを文字列として読み込むように指定
        self.df = pd.read_csv(filename, dtype={'From': str}).rename(columns=lambda x: x.strip())

    def add_threat_assessment(self):
        """'From' の電話番号に基づいて 'threat_assessment' カラムを追加する"""
        def assess_threat(row):
            phone = str(row['From'])
            if phone.startswith(('090', '080', '070')):
                return 'infected'
            elif phone.startswith('050'):
                return 'spam'
            else:
                return 'NA'

        # 'FromJapan'が'yes'であり、かつ3回以上確認できた送信元をフィルタリング
        frequent_senders = self.df[self.df['FromJapan'] == 'yes']['From'].value_counts()
        frequent_senders = frequent_senders[frequent_senders >= 3].index

        # ラベル付けの条件を満たす場合のみ threat_assessment を設定
        self.df.loc[self.df['From'].isin(frequent_senders), 'threat_assessment'] = self.df.apply(assess_threat, axis=1)
        
        # 条件を満たさない場合は 'NA' に設定
        self.df['threat_assessment'] = self.df['threat_assessment'].fillna('Error')

        return self.df

    def save_to_csv(self, data, output_threatassesment):
        """結果をCSVファイルに保存する"""
        data.to_csv(output_threatassesment, index=False)
        print(f"結果が {output_threatassesment} に保存されました")

def main():
    # データファイルを読み込む
    input_filename = 'sample.csv'
    output_threatassesment = 'threat_assesment.csv'
    analyzer = DataAnalyzer(input_filename)

    # 処理時間の計測を開始
    start_time = time.time()

    # threat_assessmentカラムを追加
    result_data = analyzer.add_threat_assessment()

    # マルウェア感染端末情報の判定を含んだcsvファイルの作成
    analyzer.save_to_csv(result_data, output_threatassesment)
    
    # 処理時間の計測を終了
    end_time = time.time()

    print(f"全プロセス完了までの時間: {end_time - start_time:.2f}秒")

if __name__ == '__main__':
    main()
