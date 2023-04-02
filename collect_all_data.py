from sec_cik_mapper import StockMapper
from secfsdstools.e_read.companycollecting import CompanyReportCollector

import pandas as pd
#use loguru for logging
from loguru import logger


# write main
def main():
    stock_mapper = StockMapper() 
    ticker_to_cik_dict = stock_mapper.ticker_to_cik
    tickers = pd.read_csv('tickers_trimmed.csv').ticker.tolist()

    for idx, ticker in enumerate(tickers):
        logger.info(f'Collecting data for {ticker}, {idx} of {len(tickers)}')
        cik = ticker_to_cik_dict.get(ticker, None)
        if not cik:
            logger.error(f'No CIK found for {ticker}')
            continue

        # get the collector
        collector = CompanyReportCollector.get_company_collector(cik=cik, forms=['10-K', '10-Q'])
        fin_df = collector.financial_statements_for_period()
        fin_df.to_csv('./data/financial_statements_{}.csv'.format(ticker), mode='a', header=False)

        logger.info(f'Collected {len(fin_df)} financial statements for {ticker}, with shape of the dataframe {fin_df.shape}')


if __name__ == '__main__':
    main()



