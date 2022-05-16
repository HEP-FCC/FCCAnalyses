window.BENCHMARK_DATA = {
  "lastUpdate": 1652708466798,
  "repoUrl": "https://github.com/HEP-FCC/FCCAnalyses",
  "entries": {
    "Benchmark": [
      {
        "commit": {
          "author": {
            "email": "34742917+kjvbrt@users.noreply.github.com",
            "name": "Juraj Smiesko",
            "username": "kjvbrt"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "e033e597772d802ded1798018b0a5885561792ee",
          "message": "Automatic macrobenchmarking (#166)\n\n* Minimal benchmark\r\n\r\n* teting benchmarking\r\n\r\n* Adding bigger is better benchmarks\r\n\r\n* Pushing the bench results to the github pages\r\n\r\n* Moving benchmarks back to test YAML\r\n\r\n* Add range and analysis info\r\n\r\n* Distinguishing prod and nightly\r\n\r\n* Installing jq\r\n\r\n* Changing ' -> \"\r\n\r\n* Introducing analysis name\r\n\r\n* Add missing space\r\n\r\n* Properly assigning names in the matrix\r\n\r\n* Adjustments to the test workflow\r\n\r\n* Using broader OSError",
          "timestamp": "2022-05-16T15:32:57+02:00",
          "tree_id": "3e62062da5ccb7e1c2d48243e28934fb9620b7bd",
          "url": "https://github.com/HEP-FCC/FCCAnalyses/commit/e033e597772d802ded1798018b0a5885561792ee"
        },
        "date": 1652708463464,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "prod | Time spent running the analysis: examples/FCCee/higgs/mH-recoil/mumu",
            "value": 19.4909245967865,
            "unit": "Seconds",
            "range": 10,
            "extra": "Analysis path: examples/FCCee/higgs/mH-recoil/mumu"
          },
          {
            "name": "prod | Time spent running the analysis: examples/FCCee/flavour/Bc2TauNu",
            "value": 16.239745616912842,
            "unit": "Seconds",
            "range": 10,
            "extra": "Analysis path: examples/FCCee/flavour/Bc2TauNu"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "34742917+kjvbrt@users.noreply.github.com",
            "name": "Juraj Smiesko",
            "username": "kjvbrt"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "e033e597772d802ded1798018b0a5885561792ee",
          "message": "Automatic macrobenchmarking (#166)\n\n* Minimal benchmark\r\n\r\n* teting benchmarking\r\n\r\n* Adding bigger is better benchmarks\r\n\r\n* Pushing the bench results to the github pages\r\n\r\n* Moving benchmarks back to test YAML\r\n\r\n* Add range and analysis info\r\n\r\n* Distinguishing prod and nightly\r\n\r\n* Installing jq\r\n\r\n* Changing ' -> \"\r\n\r\n* Introducing analysis name\r\n\r\n* Add missing space\r\n\r\n* Properly assigning names in the matrix\r\n\r\n* Adjustments to the test workflow\r\n\r\n* Using broader OSError",
          "timestamp": "2022-05-16T15:32:57+02:00",
          "tree_id": "3e62062da5ccb7e1c2d48243e28934fb9620b7bd",
          "url": "https://github.com/HEP-FCC/FCCAnalyses/commit/e033e597772d802ded1798018b0a5885561792ee"
        },
        "date": 1652708466135,
        "tool": "customBiggerIsBetter",
        "benches": [
          {
            "name": "prod | Events processed per second: examples/FCCee/higgs/mH-recoil/mumu",
            "value": 5.130592933312521,
            "unit": "Evt/s"
          },
          {
            "name": "prod | Events processed per second: examples/FCCee/flavour/Bc2TauNu",
            "value": 6.157731922589678,
            "unit": "Evt/s"
          }
        ]
      }
    ]
  }
}