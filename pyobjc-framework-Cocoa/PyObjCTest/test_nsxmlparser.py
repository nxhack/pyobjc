import Foundation
from PyObjCTools.TestSupport import TestCase, min_sdk_level
import objc


class TestNSXMLParser(TestCase):
    def testConstants(self):
        self.assertEqual(Foundation.NSXMLParserInternalError, 1)
        self.assertEqual(Foundation.NSXMLParserOutOfMemoryError, 2)
        self.assertEqual(Foundation.NSXMLParserDocumentStartError, 3)
        self.assertEqual(Foundation.NSXMLParserEmptyDocumentError, 4)
        self.assertEqual(Foundation.NSXMLParserPrematureDocumentEndError, 5)
        self.assertEqual(Foundation.NSXMLParserInvalidHexCharacterRefError, 6)
        self.assertEqual(Foundation.NSXMLParserInvalidDecimalCharacterRefError, 7)
        self.assertEqual(Foundation.NSXMLParserInvalidCharacterRefError, 8)
        self.assertEqual(Foundation.NSXMLParserInvalidCharacterError, 9)
        self.assertEqual(Foundation.NSXMLParserCharacterRefAtEOFError, 10)
        self.assertEqual(Foundation.NSXMLParserCharacterRefInPrologError, 11)
        self.assertEqual(Foundation.NSXMLParserCharacterRefInEpilogError, 12)
        self.assertEqual(Foundation.NSXMLParserCharacterRefInDTDError, 13)
        self.assertEqual(Foundation.NSXMLParserEntityRefAtEOFError, 14)
        self.assertEqual(Foundation.NSXMLParserEntityRefInPrologError, 15)
        self.assertEqual(Foundation.NSXMLParserEntityRefInEpilogError, 16)
        self.assertEqual(Foundation.NSXMLParserEntityRefInDTDError, 17)
        self.assertEqual(Foundation.NSXMLParserParsedEntityRefAtEOFError, 18)
        self.assertEqual(Foundation.NSXMLParserParsedEntityRefInPrologError, 19)
        self.assertEqual(Foundation.NSXMLParserParsedEntityRefInEpilogError, 20)
        self.assertEqual(Foundation.NSXMLParserParsedEntityRefInInternalSubsetError, 21)
        self.assertEqual(Foundation.NSXMLParserEntityReferenceWithoutNameError, 22)
        self.assertEqual(Foundation.NSXMLParserEntityReferenceMissingSemiError, 23)
        self.assertEqual(Foundation.NSXMLParserParsedEntityRefNoNameError, 24)
        self.assertEqual(Foundation.NSXMLParserParsedEntityRefMissingSemiError, 25)
        self.assertEqual(Foundation.NSXMLParserUndeclaredEntityError, 26)
        self.assertEqual(Foundation.NSXMLParserUnparsedEntityError, 28)
        self.assertEqual(Foundation.NSXMLParserEntityIsExternalError, 29)
        self.assertEqual(Foundation.NSXMLParserEntityIsParameterError, 30)
        self.assertEqual(Foundation.NSXMLParserUnknownEncodingError, 31)
        self.assertEqual(Foundation.NSXMLParserEncodingNotSupportedError, 32)
        self.assertEqual(Foundation.NSXMLParserStringNotStartedError, 33)
        self.assertEqual(Foundation.NSXMLParserStringNotClosedError, 34)
        self.assertEqual(Foundation.NSXMLParserNamespaceDeclarationError, 35)
        self.assertEqual(Foundation.NSXMLParserEntityNotStartedError, 36)
        self.assertEqual(Foundation.NSXMLParserEntityNotFinishedError, 37)
        self.assertEqual(Foundation.NSXMLParserLessThanSymbolInAttributeError, 38)
        self.assertEqual(Foundation.NSXMLParserAttributeNotStartedError, 39)
        self.assertEqual(Foundation.NSXMLParserAttributeNotFinishedError, 40)
        self.assertEqual(Foundation.NSXMLParserAttributeHasNoValueError, 41)
        self.assertEqual(Foundation.NSXMLParserAttributeRedefinedError, 42)
        self.assertEqual(Foundation.NSXMLParserLiteralNotStartedError, 43)
        self.assertEqual(Foundation.NSXMLParserLiteralNotFinishedError, 44)
        self.assertEqual(Foundation.NSXMLParserCommentNotFinishedError, 45)
        self.assertEqual(Foundation.NSXMLParserProcessingInstructionNotStartedError, 46)
        self.assertEqual(
            Foundation.NSXMLParserProcessingInstructionNotFinishedError, 47
        )
        self.assertEqual(Foundation.NSXMLParserNotationNotStartedError, 48)
        self.assertEqual(Foundation.NSXMLParserNotationNotFinishedError, 49)
        self.assertEqual(Foundation.NSXMLParserAttributeListNotStartedError, 50)
        self.assertEqual(Foundation.NSXMLParserAttributeListNotFinishedError, 51)
        self.assertEqual(Foundation.NSXMLParserMixedContentDeclNotStartedError, 52)
        self.assertEqual(Foundation.NSXMLParserMixedContentDeclNotFinishedError, 53)
        self.assertEqual(Foundation.NSXMLParserElementContentDeclNotStartedError, 54)
        self.assertEqual(Foundation.NSXMLParserElementContentDeclNotFinishedError, 55)
        self.assertEqual(Foundation.NSXMLParserXMLDeclNotStartedError, 56)
        self.assertEqual(Foundation.NSXMLParserXMLDeclNotFinishedError, 57)
        self.assertEqual(Foundation.NSXMLParserConditionalSectionNotStartedError, 58)
        self.assertEqual(Foundation.NSXMLParserConditionalSectionNotFinishedError, 59)
        self.assertEqual(Foundation.NSXMLParserExternalSubsetNotFinishedError, 60)
        self.assertEqual(Foundation.NSXMLParserDOCTYPEDeclNotFinishedError, 61)
        self.assertEqual(Foundation.NSXMLParserMisplacedCDATAEndStringError, 62)
        self.assertEqual(Foundation.NSXMLParserCDATANotFinishedError, 63)
        self.assertEqual(Foundation.NSXMLParserMisplacedXMLDeclarationError, 64)
        self.assertEqual(Foundation.NSXMLParserSpaceRequiredError, 65)
        self.assertEqual(Foundation.NSXMLParserSeparatorRequiredError, 66)
        self.assertEqual(Foundation.NSXMLParserNMTOKENRequiredError, 67)
        self.assertEqual(Foundation.NSXMLParserNAMERequiredError, 68)
        self.assertEqual(Foundation.NSXMLParserPCDATARequiredError, 69)
        self.assertEqual(Foundation.NSXMLParserURIRequiredError, 70)
        self.assertEqual(Foundation.NSXMLParserPublicIdentifierRequiredError, 71)
        self.assertEqual(Foundation.NSXMLParserLTRequiredError, 72)
        self.assertEqual(Foundation.NSXMLParserGTRequiredError, 73)
        self.assertEqual(Foundation.NSXMLParserLTSlashRequiredError, 74)
        self.assertEqual(Foundation.NSXMLParserEqualExpectedError, 75)
        self.assertEqual(Foundation.NSXMLParserTagNameMismatchError, 76)
        self.assertEqual(Foundation.NSXMLParserUnfinishedTagError, 77)
        self.assertEqual(Foundation.NSXMLParserStandaloneValueError, 78)
        self.assertEqual(Foundation.NSXMLParserInvalidEncodingNameError, 79)
        self.assertEqual(Foundation.NSXMLParserCommentContainsDoubleHyphenError, 80)
        self.assertEqual(Foundation.NSXMLParserInvalidEncodingError, 81)
        self.assertEqual(Foundation.NSXMLParserExternalStandaloneEntityError, 82)
        self.assertEqual(Foundation.NSXMLParserInvalidConditionalSectionError, 83)
        self.assertEqual(Foundation.NSXMLParserEntityValueRequiredError, 84)
        self.assertEqual(Foundation.NSXMLParserNotWellBalancedError, 85)
        self.assertEqual(Foundation.NSXMLParserExtraContentError, 86)
        self.assertEqual(Foundation.NSXMLParserInvalidCharacterInEntityError, 87)
        self.assertEqual(Foundation.NSXMLParserParsedEntityRefInInternalError, 88)
        self.assertEqual(Foundation.NSXMLParserEntityRefLoopError, 89)
        self.assertEqual(Foundation.NSXMLParserEntityBoundaryError, 90)
        self.assertEqual(Foundation.NSXMLParserInvalidURIError, 91)
        self.assertEqual(Foundation.NSXMLParserURIFragmentError, 92)
        self.assertEqual(Foundation.NSXMLParserNoDTDError, 94)
        self.assertEqual(Foundation.NSXMLParserDelegateAbortedParseError, 512)

        self.assertIsInstance(Foundation.NSXMLParserErrorDomain, str)

        self.assertEqual(Foundation.NSXMLParserResolveExternalEntitiesNever, 0)
        self.assertEqual(Foundation.NSXMLParserResolveExternalEntitiesNoNetwork, 1)
        self.assertEqual(Foundation.NSXMLParserResolveExternalEntitiesSameOriginOnly, 2)
        self.assertEqual(Foundation.NSXMLParserResolveExternalEntitiesAlways, 3)

    def testMethods(self):
        self.assertArgIsBOOL(Foundation.NSXMLParser.setShouldProcessNamespaces_, 0)
        self.assertArgIsBOOL(
            Foundation.NSXMLParser.setShouldReportNamespacePrefixes_, 0
        )
        self.assertArgIsBOOL(
            Foundation.NSXMLParser.setShouldResolveExternalEntities_, 0
        )
        self.assertResultIsBOOL(Foundation.NSXMLParser.shouldProcessNamespaces)
        self.assertResultIsBOOL(Foundation.NSXMLParser.shouldReportNamespacePrefixes)
        self.assertResultIsBOOL(Foundation.NSXMLParser.shouldResolveExternalEntities)
        self.assertResultIsBOOL(Foundation.NSXMLParser.parse)

    @min_sdk_level("10.6")
    def testProtocols(self):
        objc.protocolNamed("NSXMLParserDelegate")
