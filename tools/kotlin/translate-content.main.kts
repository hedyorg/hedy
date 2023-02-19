#!/usr/bin/env kotlin

@file:DependsOn("com.github.ajalt.clikt:clikt-jvm:3.5.1")
@file:DependsOn("org.yaml:snakeyaml:1.33")
@file:DependsOn("com.deepl.api:deepl-java:1.1.0")

import com.deepl.api.Formality
import com.deepl.api.TextTranslationOptions
import com.deepl.api.Translator
import com.github.ajalt.clikt.core.CliktCommand
import com.github.ajalt.clikt.parameters.options.help
import com.github.ajalt.clikt.parameters.options.option
import com.github.ajalt.clikt.parameters.options.required
import com.github.ajalt.clikt.parameters.types.file
import org.yaml.snakeyaml.DumperOptions
import org.yaml.snakeyaml.Yaml
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

        val options = DumperOptions().apply {
            isExplicitStart = true
            defaultFlowStyle = DumperOptions.FlowStyle.BLOCK
            defaultScalarStyle = DumperOptions.ScalarStyle.PLAIN
        }
        val yaml = Yaml(options)
        // Call DeepL file by file to avoid multiple network calls
        filesToTranslate.forEach { file ->
            val parsedYaml = yaml.load<MutableMap<Any, Any>>(file.readText())

            // Hopefully no such values in the text
            val translationSeparator = "#######"
            val keyValueSeparator = "::::::"
            // Result will be text constructed like
            // <Yaml Scalar hash>::::::<Text to translate>######<Yaml Scalar Text>...
            // Assumption that DeepL will not translate separators and hashes
            // DeepL also keeps the new lines present in text (which is nice)
            val textToTranslate = parsedYaml.toScalarList()
                .joinToString(translationSeparator) { value ->
                    "${value.hashCode()}$keyValueSeparator$value"
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

            parsedYaml.translate(mapHashToTranslated)

            file.setWritable(true)
            val yamlString = yaml.dump(parsedYaml)
            file.writeText(yamlString)
        }
    }
}

@Suppress("UNCHECKED_CAST")
fun Map<Any, Any>.toScalarList(): List<String> = map { (key, value) ->
    when (value) {
        is String -> listOf(value)
        is Map<*, *> -> (value as Map<Any, Any>).toScalarList()
        else -> emptyList()
    }
}.flatten()

@Suppress("UNCHECKED_CAST")
fun MutableMap<Any, Any>.translate(translations: Map<Int, String>) {
    forEach { (key, value) ->
        when (value) {
            is String -> put(key, translations[value.hashCode()]!!)
            is Map<*, *> -> (value as MutableMap<Any, Any>).translate(translations)
            else -> {
                // nothing
            }
        }
    }
}

TranslateContent().main(args)
