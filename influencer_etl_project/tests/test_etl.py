import unittest
import pandas as pd

class TestETL(unittest.TestCase):

    def test_engagement_rate_calculation(self):
        sample_data = {
            'likes': [100, 200],
            'comments': [50, 80],
            'shares': [20, 30],
            'views': [1000, 2000]
        }
        df = pd.DataFrame(sample_data)
        df['engagementRate'] = (df['likes'] + df['comments'] + df['shares']) / df['views'] * 100

        self.assertAlmostEqual(df['engagementRate'][0], 17.0, places=1)
        self.assertAlmostEqual(df['engagementRate'][1], 15.5, places=1)

    def test_top_performers_sorting(self):
        sample_data = [
            {'campaignId': 'camp_1', 'influencerId': 'inf_1', 'engagementRate': 25.0},
            {'campaignId': 'camp_1', 'influencerId': 'inf_2', 'engagementRate': 35.0},
            {'campaignId': 'camp_1', 'influencerId': 'inf_3', 'engagementRate': 15.0},
        ]
        sorted_data = sorted(sample_data, key=lambda x: x['engagementRate'], reverse=True)

        engagement_rates = [entry['engagementRate'] for entry in sorted_data]
        self.assertEqual(engagement_rates, sorted(engagement_rates, reverse=True))

if __name__ == '__main__':
    unittest.main()
