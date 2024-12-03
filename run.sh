pip install .
echo "\n\n"
echo "now testing mutpy"
echo "\n"
bin/mut.py --target example/simple.py --unit-test example/test/simple_good_test_pytest.py --mutation-number 1 -m --debug
# bin/mut.py --target example/simple.py --unit-test example/test/simple_good_test.py -m --debug
