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

val DEEPL_REQUEST_LIMIT = 1024 * 100

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

        val dumperOptions = DumperOptions().apply {
            defaultFlowStyle = DumperOptions.FlowStyle.BLOCK
        }
        val yaml = Yaml(dumperOptions)
        // Call DeepL file by file to avoid multiple network calls
        filesToTranslate.forEach { file ->
            echo("Translating ${file.canonicalPath}")
            val parsedYaml = yaml.load<MutableMap<Any, Any>>(file.readText())

            // Hopefully no such values in the text
            val translationSeparator = "#######"
            val keyValueSeparator = "^^^^^^^^"
            // Result will be text constructed like
            // <Yaml Scalar hash>::::::<Text to translate>######<Yaml Scalar Text>...
            // Assumption that DeepL will not translate separators and hashes
            // DeepL also keeps the new lines present in text (which is nice)
            val textToTranslate = parsedYaml.toScalarList()
                .joinToString(translationSeparator) { value ->
                    "${value.hashCode()}$keyValueSeparator$value"
                }

            val translator = Translator(authKey)
            val translationOptions = TextTranslationOptions().apply {
                isPreserveFormatting = true
                formality = Formality.PreferMore
            }
            // Dummy call without catching errors
            if (textToTranslate.toByteArray().size < DEEPL_REQUEST_LIMIT) {
                val result = translator.translateText(
                    textToTranslate,
                    "en",
                    language,
                    translationOptions
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
                echo("Done!")
            } else {
                echo("Translation is too big")
            }
        }
    }
}

fun Map<*, *>.toScalarList(): List<String> = map { (_, value) ->
    when (value) {
        is String -> listOf(value)
        is Map<*, *> -> value.toScalarList()
        is List<*> -> value.toScalarList()
        else -> emptyList()
    }
}.flatten()


fun List<*>.toScalarList(): List<String> = map { value ->
    when (value) {
        is String -> listOf(value)
        is Map<*, *> -> value.toScalarList()
        is List<*> -> value.toScalarList()
        else -> emptyList()
    }
}.flatten()

@Suppress("UNCHECKED_CAST")
fun MutableMap<Any, Any>.translate(translations: Map<Int, String>) {
    forEach { (key, value) ->
        when (value) {
            is String -> put(key, translations[value.hashCode()]!!)
            is MutableMap<*, *> -> (value as MutableMap<Any, Any>).translate(translations)
            is MutableList<*> -> (value as MutableList<Any>).translate(translations)
            else -> {
                // nothing
            }
        }
    }
}

@Suppress("UNCHECKED_CAST")
fun MutableList<Any>.translate(translations: Map<Int, String>): Unit = forEachIndexed { index, value ->
    when (value) {
        is String -> set(index, translations[value.hashCode()]!!)
        is MutableMap<*, *> -> (value as MutableMap<Any, Any>).translate(translations)
        is MutableList<*> -> (value as MutableList<Any>).translate(translations)
        else -> {
            // nothing
        }
    }
}

TranslateContent().main(args)
