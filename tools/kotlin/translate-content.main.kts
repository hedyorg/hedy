#!/usr/bin/env kotlin

@file:DependsOn("com.github.ajalt.clikt:clikt-jvm:3.5.1")
@file:DependsOn("com.charleskorn.kaml:kaml-jvm:0.51.0")
@file:DependsOn("com.deepl.api:deepl-java:1.1.0")

import com.charleskorn.kaml.*
import com.deepl.api.*
import com.github.ajalt.clikt.core.CliktCommand
import com.github.ajalt.clikt.parameters.options.help
import com.github.ajalt.clikt.parameters.options.option
import com.github.ajalt.clikt.parameters.options.required
import com.github.ajalt.clikt.parameters.types.file
import java.io.File

class TranslateContent : CliktCommand(help = "Translate content file with DeepL") {
    private val contentFileOrRootDir: File by option("--content")
        .help("Root directory for files search or file to translate")
        .file()
        .required()

    private val language by option("--language")
        .help("ISO code for language to translate")
        .required()

    private val authKey by option("--deepl-key")
        .help("DeepL auth key")
        .required()

    override fun run() {
        val filesToTranslate = if (contentFileOrRootDir.isFile) {
            sequenceOf(contentFileOrRootDir)
        } else {
            contentFileOrRootDir.walkTopDown()
                .filter { file ->
                    file.name.startsWith(language)
                }
        }

        // Call DeepL file by file to avoid multiple network calls
        filesToTranslate.forEach { file ->
            val parsedYaml = Yaml.default.parseToYamlNode(file.readText())

            // Hopefully no such values in the text
            val translationSeparator = "#######"
            val keyValueSeparator = "::::::"
            // Result will be text constructed like
            // <Yaml Scalar hash>::::::<Text to translate>######<Yaml Scalar Text>...
            // Assumption that DeepL will not translate separators and hashes
            // DeepL also keeps the new lines present in text (which is nice)
            val textToTranslate = parsedYaml.yamlMap
                .entries
                .values
                .map { it.toScalarList() }
                .flatten()
                .associateWith { it.content }
                .entries
                .joinToString(translationSeparator) { (key, value) ->
                    "${key.hashCode()}$keyValueSeparator$value"
                }

            // Dummy call without catching errors
            val translator = Translator(authKey)
            val result = translator.translateText(
                textToTranslate,
                "en",
                language,
                TextTranslationOptions().apply {
                    isPreserveFormatting = true
                    formality = Formality.PreferMore
                }
            )
            val mapHashToTranslated = result.text
                .split(translationSeparator)
                .associate {
                    val (hash, value) = it.split(keyValueSeparator)
                    hash.toInt() to value
                }

            // Fortunately/Unfortunately the parsed structure is read only
            // so I have to reconstruct it with replaced translated text
            val translatedYaml = parsedYaml.yamlMap
                .entries
                .map {
                    it.key to it.value.translate(mapHashToTranslated)
                }.toMap()
                .let {
                    YamlMap(it, parsedYaml.yamlMap.path)
                }

            file.setWritable(true)
//            file.writeText(Yaml.default.encodeToString(translatedYaml))
        }
    }
}

fun YamlNode.toScalarList(): List<YamlScalar> = when (this) {
    is YamlList -> items.map { it.toScalarList() }.flatten()
    is YamlMap -> entries.map { it.value.toScalarList() }.flatten()
    is YamlNull -> emptyList()
    is YamlScalar -> listOf(this)
    is YamlTaggedNode -> innerNode.toScalarList()
}

fun YamlNode.translate(translations: Map<Int, String>): YamlNode = when (this) {
    is YamlList -> YamlList(items.map { it.translate(translations) }, path)
    is YamlMap -> YamlMap(this.entries.map { it.key to it.value.translate(translations) }.toMap(), path)
    is YamlNull -> this
    is YamlScalar -> YamlScalar(translations[hashCode()]!!, path)
    is YamlTaggedNode -> YamlTaggedNode(tag, innerNode.translate(translations))
}

TranslateContent().main(args)
