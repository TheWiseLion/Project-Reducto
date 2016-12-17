import { StaticPage } from './app.po';

describe('static App', function() {
  let page: StaticPage;

  beforeEach(() => {
    page = new StaticPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
