# Matchmaker

Seller to buyer matching algorithm.


## Running the application

The application can be run by invoking `main.py` directly. It is compatible with both python 2 and python 3.

Running the application will print an admittedly hard to read printout of each seller, along with an indented list below consisting of all of it's matched buyers, ranked accordingly.  The weight of the match will be listed at the beginning of each buyer's row.

```bash
$ python main.py
<seller info>
  <buyer rank>: <buyer info>
  <buyer rank>: <buyer info>
  <buyer rank>: <buyer info>

<seller info>
  <buyer rank>: <buyer info>
  <buyer rank>: <buyer info>
```

This can end up being a little bit of a pain to actually read.

```bash
$ python main.py

[type=seller id=eab9f092-28fd-4eab-b074-76e809efb4c1 geography_ids={112, 114, 116} industry_ids={257, 258, 251, 261}]
	4: [type=buyer id=050130a0-3afa-4dc3-a0df-8302a64cb402 geography_ids={104, 107, 111, 114, 116, 119, 121, 123} industry_ids={251, 269, 254}]
	4: [type=buyer id=69214e60-a21e-409b-8b20-a53d7610feb0 geography_ids={107, 112, 113, 114, 115, 118, 123} industry_ids={264, 251}]
	4: [type=buyer id=9c1d538b-ab79-4c69-96d2-ea0c0977fa24 geography_ids={101, 102, 104, 109, 111, 112, 114, 120, 123, 125} industry_ids={265, 262, 257}]
	2: [type=buyer id=58574613-3b53-47b0-973d-7aabe9185f28 geography_ids={121, 123, 116} industry_ids={258, 259, 261, 265, 267, 252, 254}]
	2: [type=buyer id=781c4499-955d-44f8-897d-d49f20f50a6e geography_ids={106, 109, 111, 112, 117, 119, 120, 123, 125} industry_ids={256, 267, 269, 273, 251}]
	2: [type=buyer id=5ed9dad3-2cf6-4e72-b374-ad5b78fcac28 geography_ids={104, 112, 113, 117, 118, 119} industry_ids={272, 258, 270}]
	2: [type=buyer id=a3af8d60-9c70-4c1a-9e25-fc6107a11d76 geography_ids={102, 111, 116, 117, 119, 121, 122, 123, 125} industry_ids={272, 257, 274, 255}]
	2: [type=buyer id=0829cd31-55c1-4ffe-8471-f4ab31c5d466 geography_ids={105, 107, 110, 116, 117, 120, 121, 123} industry_ids={257, 258, 263, 267, 269, 251}]
	2: [type=buyer id=e110129c-dc4e-4452-ac4c-7a1cef95ad68 geography_ids={101, 104, 107, 108, 110, 111, 116, 120} industry_ids={261, 265, 275, 252, 253}]
	2: [type=buyer id=d03d8253-4682-437f-8c39-91f1dfdcc677 geography_ids={112, 123} industry_ids={261, 252, 253, 255}]
	2: [type=buyer id=640eb9fa-b151-4784-bdd1-e17c2edc7ff5 geography_ids={101, 102, 105, 107, 116, 118, 119, 122} industry_ids={256, 260, 270, 275, 251}]
	2: [type=buyer id=9f01c38b-62e3-4326-bad0-f50221b2d1bf geography_ids={112, 107, 104, 103} industry_ids={259, 261, 264, 265, 266, 273, 275}]
	2: [type=buyer id=ccae0885-d178-4050-a62e-164d6366ba8c geography_ids={101, 104, 106, 108, 112, 115, 120, 125} industry_ids={259, 264, 265, 272, 251, 255}]
	2: [type=buyer id=d8cafbfb-7ad9-4530-b12d-641a1effe658 geography_ids={102, 103, 105, 106, 107, 111, 112, 122} industry_ids={256, 261, 262, 264, 268, 270, 272}]
	2: [type=buyer id=e1a494be-6016-4695-977b-243e8b2a0035 geography_ids={112, 109, 118} industry_ids={256, 257, 253, 262}]
	2: [type=buyer id=dd13e6ea-f6b5-4c1c-a78b-fa8f0c4e843d geography_ids={101, 102, 110, 116, 119} industry_ids={258, 259, 260, 266, 270, 252, 255}]

... omitted for brevity ...
```

## Output

You can see the full output for each of the three implementations here:

* [Default](https://github.com/mpdavis/matchmaker/blob/master/output/default.md) - Geography and industry weighted equally
* [Geography Only](https://github.com/mpdavis/matchmaker/blob/master/output/geography_only.md) - Only geography taken into account for ranking, industry ignored
* [Industry Only](https://github.com/mpdavis/matchmaker/blob/master/output/industry_only.md) - Only industry taken into account for ranking, geography ignored

## Ranking Algorithm

There are a handful options for determining how matches are ranked. This is accomplished by weighing geography id matches and industry matches separately.  Those weights can be adjusted in order to tweak the end ranking as needed.

My ranking algorithm is as such:

    ((number of geography_id matches - geography_id misses) * geography_weight) + ((number of industry_id matches - industry_id misses) * industry_weight)

The general theory is that the more geography_ids and industry_ids that a buyer and seller have in common, the better fit they will be. We then dock the matched pair for each id that it does not have in common.  The reason for this is to get the best match possible. If a buyer is an exact match for a seller, they should be ranked above a buyer than simply has a huge number of ids they are looking for.

The geography weight and the industry weight can be adjusted independently in order to further tweak the rankings as needed.

Different matchers have been implemented in the [matcher](https://github.com/mpdavis/matchmaker/blob/master/matcher.py) module to show the altering of the weights.  These matchers are not run by default. [main.py](https://github.com/mpdavis/matchmaker/blob/master/main.py) can be updated to run with different matchers.

Note: Ranking only comes into play when a buyer and seller have been matched, which requires at least one common geography_id and one common industry_id.

One of the largest drawbacks of my choice of algorithm is the fact that so many matches end up with the same ranking. As is, rankings for matches with the same value are non-deterministic. Being non-deterministic when ranking is not ideal. If a seller sees that the order of the rankings that they are shown changes, then they would be less likely to trust the ranking.  To mitigate this, I would find a simple, deterministic way of ordering matches with the same ranking, such as alphabetically by the id.

## Running tests

The (minimal) tests can be run via pytest.

If you don't have pytest installed, it can be installed via pip.

```bash
pip install pytest
```

All tests should pass successfully.

```bash
$ py.test
==================================== test session starts =====================================
platform darwin -- Python 3.6.0, pytest-3.1.3, py-1.4.34, pluggy-0.4.0
rootdir: /Users/michael/workspace/mpdavis/matchmaker, inifile:
collected 5 items

tests/test_matcher.py ...
tests/test_participant.py ..

================================== 5 passed in 0.08 seconds ==================================```
