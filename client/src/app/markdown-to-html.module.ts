import { NgModule } from "@angular/core";
import { MarkdownToHtmlPipe } from "./markdown-to-html.pipe";

@NgModule({
  declarations: [MarkdownToHtmlPipe],
  exports: [MarkdownToHtmlPipe],
})
export class MarkdownToHtmlModule {}
