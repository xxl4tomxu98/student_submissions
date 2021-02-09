import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import Sum from './Sum';
import { render, fireEvent, cleanup, wait } from '@testing-library/react';
import { XMLHttpRequest } from 'xmlhttprequest';
global.XMLHttpRequest = XMLHttpRequest;
import fetchMock from 'fetch-mock';
fetchMock.config.fallbackToNetwork = true;

import 'jest-dom/extend-expect';


const term = "4000"
const renderApp = () => render(<App term={term}/>);

beforeEach(() => {
});

afterEach(() => {
  // restore fetch() to its native implementation
  fetchMock.restore();
  cleanup();
});

describe('true is truthy and false is falsy', () => {
  test('true is truthy', () => {
    expect(true).toBe(true);
  });

  test('false is falsy', () => {
    expect(false).toBe(false);
  });
});

describe('sum', () => {
  test('sums up two values', () => {
    expect(Sum(2, 4)).toBe(6);
  });
});

describe('AppTest', () => {
    test('renders App component', async () => {
        const response =  [
                            {
                              all_tags: [],
                              avg_rating: 3.0,
                              genres: [
                                "Adventure",
                                "Drama"
                              ],
                              imdb_tmdb: [
                                86993,
                                2669
                              ],
                              movie_id: 4000,
                              rating_count: 3,
                              release_year: "1984",
                              tag_count: 0,
                              title: "Bounty, The (1984)"
                            }
                          ]

        fetchMock.getOnce("*", JSON.stringify(response));
        //screen.getByText('Hello React');
        // Without screen, you need to provide a container:
        const { getByTestId, queryByTestId, queryAllByTestId } = renderApp();
        // const container = document.querySelector('#app')
        // const inputNode2 = getByText(container, 'Hello React')


        await wait(() => {
            const pageTitle = queryByTestId('app-title');
            //const pageButtons = queryByAllTestId('page-button');
            expect(pageTitle).toHaveTextContent("Hello, My Movielens Challenge.");
            //expect(pageButtons).toHaveLength(response.length);

        });
    });
});
