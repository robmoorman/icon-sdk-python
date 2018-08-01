import unittest
import os

from IconService.wallet.wallet import KeyWallet
from IconService.exception import KeyStoreException


class TestWalletStore(unittest.TestCase):

    TEST_DIR = os.path.abspath("keystore_file")
    TEST_KEYSTORE_FILE_NEW_PASSWORD = "Adas21312**"
    TEST_KEYSTORE_FILE_WRONG_PASSWORD = "Adas2**"
    TEST_NEW_PATH = os.path.join(TEST_DIR, "test_new_keystore.txt")
    TEST_WRONG_PATH = os.path.join(TEST_DIR, "unknown_folder", "test_keystore.txt")

    def test_wallet_store_successfully(self):
        """Creates a wallet and validate the wallet."""
        wallet = KeyWallet.create()
        wallet.store(self.TEST_NEW_PATH, self.TEST_KEYSTORE_FILE_NEW_PASSWORD)
        wallet2 = wallet.load(self.TEST_NEW_PATH, self.TEST_KEYSTORE_FILE_NEW_PASSWORD)

        self.assertEqual(wallet.get_address(), wallet2.get_address())
        self.assertEqual(wallet.get_private_key(), wallet2.get_private_key())

    def test_wallet_store_on_the_wrong_path(self):
        """Case When storing a keystore file on a wrong path that does not exist."""
        wallet = KeyWallet.create()
        self.assertRaises(KeyStoreException, wallet.store, self.TEST_WRONG_PATH, self.TEST_KEYSTORE_FILE_NEW_PASSWORD)

    def test_wallet_store_with_wrong_password(self):
        """Case when entering a invalid password."""
        wallet = KeyWallet.create()
        self.assertRaises(KeyStoreException, wallet.store, self.TEST_NEW_PATH, self.TEST_KEYSTORE_FILE_WRONG_PASSWORD)

    def test_wallet_store_overwriting(self):
        """Case when overwriting the existing keystore file."""
        wallet = KeyWallet.create()
        wallet.store(self.TEST_NEW_PATH, self.TEST_KEYSTORE_FILE_NEW_PASSWORD)

        wallet2 = KeyWallet.create()
        self.assertRaises(KeyStoreException, wallet2.store, self.TEST_NEW_PATH, self.TEST_KEYSTORE_FILE_NEW_PASSWORD)

    def tearDown(self):
        # Remove used file.
        if os.path.isfile(self.TEST_NEW_PATH):
            os.remove(self.TEST_NEW_PATH)