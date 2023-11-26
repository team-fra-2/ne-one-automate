from rule_engine.functions import is_typo_correction


def test_is_typo_correction():
    original_sentence = "Thiss is a corect sentnce."
    updated_sentence = "This is a correct sentence."
    assert is_typo_correction(original_sentence, updated_sentence) is True


def test_is_typo_correction_2():
    original_sentence = "High-precisoin robotics compnents, sesnitive to temprature and humidty, paked in anti-sttic containrs"
    updated_sentence = "High-precision robotics components, sensitive to temperature and humidity, packs in anti-static containers"
    assert is_typo_correction(original_sentence, updated_sentence) is True
