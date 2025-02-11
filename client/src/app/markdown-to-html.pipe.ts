import { Pipe, PipeTransform } from "@angular/core";

@Pipe({
  name: "markdownToHtml",
})
export class MarkdownToHtmlPipe implements PipeTransform {
  transform(value: any): string {
    if (value === null || value === undefined) {
      return "";
    }

    if (typeof value === "string") {
      return this.convertMarkdownToHtml(value);
    }

    if (typeof value === "object") {
      return this.convertMarkdownToHtml(JSON.stringify(value));
    }

    return "";
  }

  private convertMarkdownToHtml(text: string): string {
    if (!text) return "";

    let convertedText = text.replaceAll(/(##\s)(.*)/g, "<h2>$2</h2>");

    convertedText = convertedText.replaceAll(
      /\*\*(.*?)\*\*/g,
      "<strong>$1</strong>"
    );

    convertedText = convertedText.replaceAll(/\n/g, "<br>");

    convertedText = convertedText.replaceAll("*", "");

    convertedText = convertedText.replaceAll("```ss", "");

    return convertedText;
  }
}
